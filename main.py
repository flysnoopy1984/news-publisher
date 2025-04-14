import json
from pathlib import Path
import logging
from datetime import datetime
from typing import List, Dict

from db.dbNewsInfos import db_news_infos
from db.dbPushInfoLatest import db_push_info_latest
from api.newsApi import news_api

class NewsPublisher:
    """
    新闻发布管理器
    """
    def __init__(self):
        self.sources = []
        self.initialize()

    def initialize(self):
        """
        初始化函数，加载数据源配置
        """
        try:
            source_file = Path(__file__).parent / "news-source.json"
            with open(source_file, 'r', encoding='utf-8') as f:
                self.sources = json.load(f)
            logging.info(f"成功加载 {len(self.sources)} 个新闻源")
        except Exception as e:
            logging.error(f"加载新闻源配置文件失败: {e}")
            self.sources = []

    def push_news(self):
        """
        推送新闻业务逻辑
        1. 遍历数据源
        2. 对每个数据源：
           - 获取数据库中的最新记录
           - 获取API的最新数据
           - 比较并插入新数据
           - 创建推送记录
        """
        for source in self.sources:
            source_id = source["id"]
            source_name = source["name"]
            
            # 获取数据库中的最新记录
            db_records = db_news_infos.get_latest_by_sourceId(source_id)
            db_orig_ids = set()
            if db_records:
                db_orig_ids = {record[2] for record in db_records}  # orig_Id在结果的第3个位置
            
            # 获取API的最新数据
            api_data = news_api.fetch_news_by_id(source_id)
            if not api_data or api_data.get("status") != "success":
                logging.error(f"获取新闻源 {source_id} 的API数据失败")
                continue
                
            # 处理新数据
            for item in api_data["items"]:
                orig_id = str(item["id"])
                if orig_id not in db_orig_ids:
                    # 插入新的新闻记录
                    news_data = {
                        "orig_Id": orig_id,
                        "title": item["title"],
                        "url": item["url"],
                        "sourceId": source_id
                    }
                    
                    inserted_id = db_news_infos.insert_single_news(news_data)
                    if inserted_id:
                        # 创建推送记录
                        push_data = {
                            "sourceId": source_id,
                            "sourceName": source_name,
                            "newsInfoId": str(inserted_id),
                            "newsType": "news",
                            "status": 0
                        }
                        db_push_info_latest.insert_single_push_info(push_data)
            
        logging.info("完成新闻推送处理")

# 创建发布器实例
news_publisher = NewsPublisher()

async def scheduled(event, env, ctx):
    """
    Cloudflare Workers 定时任务入口函数
    """
    try:
        news_publisher.push_news()
        return {"status": "success", "message": "新闻推送任务执行完成"}
    except Exception as e:
        logging.error(f"新闻推送任务执行失败: {e}")
        return {"status": "error", "message": str(e)}
