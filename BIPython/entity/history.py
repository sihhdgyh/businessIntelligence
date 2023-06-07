from datetime import datetime

from database import db


class History(db.Model):
    # 设置表名
    __tablename__ = 'history'
    # 创建数据库表字段
    # db.Column(类型，约束)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.String(200))
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
        }

    @staticmethod
    def jsonformatList(historyList):
        List=[]
        for item in historyList:
            List.append(History.jsonformat(item))

        return List