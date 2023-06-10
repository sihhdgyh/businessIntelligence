from datetime import datetime

from database import db


class categoryDayClick(db.Model):
    # 设置表名
    __tablename__ = 'categoryDayClick1'
    # 创建数据库表字段
    # db.Column(类型，约束)
    id = db.Column(db.String(200), primary_key=True)
    category = db.Column(db.String(200))
    exposureTime = db.Column(db.Date)
    totalTime = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    # def jsonformat(self):
    #     return {
    #         "id": self.id,
    #         "userId": self.userId,
    #         "newsId": self.newsId,
    #         "dwellTime": self.dwellTime,
    #         "exposureTime": str(self.exposureTime),
    #     }
    #
    # @staticmethod
    # def jsonformatList(historyList):
    #     List=[]
    #     for item in historyList:
    #         List.append(History.jsonformat(item))
    #
    #     return List