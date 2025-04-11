from datetime import datetime
from .dbManager import db_manager
import logging

class DBNewsInfos:
    """
    处理news_infos表的批量写入操作
    """
    def __init__(self):
        self.db = db_manager

    def batch_insert_news(self, news_list):
        """
        批量插入新闻信息
        
        Args:
            news_list: 包含新闻信息的列表，每个元素是一个字典，包含：
                - newsId: 新闻ID
                - title: 新闻标题
                - url: 新闻链接
                
        Returns:
            bool: 插入是否成功
        """
        if not news_list:
            logging.warning("新闻列表为空，无需插入")
            return True

        current_time = datetime.now()
        
        # 准备批量插入的数据
        insert_data = [
            (
                news['newsId'],
                news['title'],
                news['url'],
                current_time
            )
            for news in news_list
        ]
        
        # SQL语句
        sql = """
            INSERT INTO news_infos 
            (newsId, title, url, createDateTime)
            VALUES (%s, %s, %s, %s)
        """
        
        try:
            # 执行批量插入
            success = self.db.executemany(sql, insert_data)
            if success:
                self.db.commit()
                logging.info(f"成功批量插入 {len(news_list)} 条新闻数据")
                return True
            else:
                self.db.rollback()
                logging.error("批量插入新闻数据失败")
                return False
                
        except Exception as e:
            self.db.rollback()
            logging.error(f"批量插入新闻数据时发生错误: {e}")
            return False

    def get_latest_by_newsid(self, news_id, limit=30):
        """
        获取指定newsId的最新记录
        
        Args:
            news_id: 新闻ID
            limit: 返回的记录数量，默认30条
            
        Returns:
            list: 返回查询结果列表，每个元素是一个元组 (id, newsId, title, url, createDateTime)
                  如果发生错误返回None
        """
        sql = """
            SELECT id, newsId, title, url, createDateTime 
            FROM news_infos 
            WHERE newsId = %s 
            ORDER BY createDateTime DESC 
            LIMIT %s
        """
        
        try:
            success = self.db.execute(sql, (news_id, limit))
            if success:
                results = self.db.fetchall()
                return results
            else:
                logging.error(f"查询新闻ID {news_id} 的数据失败")
                return None
                
        except Exception as e:
            logging.error(f"查询新闻数据时发生错误: {e}")
            return None

# 创建实例供直接导入使用
db_news_infos = DBNewsInfos()
