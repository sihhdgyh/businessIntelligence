from datetime import datetime

from database import db


class newsCategoryHistory(db.Model):
    # 设置表名
    __tablename__ = 'newsCategoryHistory'
    # 创建数据库表字段
    # db.Column(类型，约束)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.String(200))
    category = db.Column(db.String(200))
    newsId = db.Column(db.String(200))
    dwellTime = db.Column(db.Integer)
    exposureTime = db.Column(db.DateTime, default=datetime.now)

    def jsonformat(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "newsId": self.newsId,
            "dwellTime": self.dwellTime,
            "exposureTime": str(self.exposureTime),
            'category':self.category
        }

    @staticmethod
    def jsonformatList(historyList):
        List=[]
        for item in historyList:
            List.append(newsCategoryHistory.jsonformat(item))

        return List