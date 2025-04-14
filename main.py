import json
from pathlib import Path
import logging
import os
from datetime import datetime
from typing import List, Dict

from db.dbNewsInfos import db_news_infos
from db.dbPushInfoLatest import db_push_info_latest
from api.newsApi import news_api

# 确保logs目录存在
os.makedirs('logs', exist_ok=True)

# 配置日志
log_file = f'logs/news_publisher_{datetime.now().strftime("%Y-%m-%d")}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

# 获取主logger
logger = logging.getLogger('NewsPublisher')

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
            logger.info(f"成功加载 {len(self.sources)} 个新闻源")
        except Exception as e:
            logger.error(f"加载新闻源配置文件失败: {e}", exc_info=True)
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
        logger.info("开始执行新闻推送任务...")
        for source in self.sources:
            source_id = source["id"]
            source_name = source["name"]
            logger.info(f"处理新闻源: {source_name}({source_id})")
            
            # 获取数据库中的最新记录
            db_records = db_news_infos.get_latest_by_sourceId(source_id)
            db_orig_ids = set()
            if db_records:
                db_orig_ids = {record[2] for record in db_records}  # orig_Id在结果的第3个位置
                logger.info(f"从数据库获取到 {len(db_records)} 条已存在的记录")
            
            # 获取API的最新数据
            api_data = news_api.fetch_news_by_id(source_id)
            if not api_data or api_data.get("status") != "success":
                logger.error(f"获取新闻源 {source_id} 的API数据失败")
                continue
                
            # 处理新数据
            new_items = [item for item in api_data["items"] if str(item["id"]) not in db_orig_ids]
            logger.info(f"发现 {len(new_items)} 条新新闻")
            
            if new_items:
                # 删除已发布的信息
                db_push_info_latest.delete_by_type_and_source(source_id)
           

            for item in new_items:
                orig_id = str(item["id"])
                # 插入新的新闻记录
                news_data = {
                    "orig_Id": orig_id,
                    "title": item["title"],
                    "url": item["url"],
                    "sourceId": source_id
                }
                
                inserted_id = db_news_infos.insert_single_news(news_data)
                if inserted_id:
                    logger.info(f"成功插入新闻: {item['title'][:30]}...")
                    # 创建推送记录
                    push_data = {
                        "sourceId": source_id,
                        "sourceName": source_name,
                        "newsInfoId": str(inserted_id),
                        "newsType": "news",
                        "status": 0
                    }
                    push_result = db_push_info_latest.insert_single_push_info(push_data)
                    if push_result:
                        logger.info(f"成功创建推送记录，ID: {push_result}")
            
        logger.info("完成新闻推送处理")

# 创建发布器实例
news_publisher = NewsPublisher()

if __name__ == "__main__":
    try:
        news_publisher.push_news()
        logger.info("任务执行完成")
    except Exception as e:
        logger.error("任务执行失败", exc_info=True)
        raise
