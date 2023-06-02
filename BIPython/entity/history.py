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
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    minute = db.Column(db.Integer)
    seconds = db.Column(db.Integer)

    def jsonformat(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "newsId": self.newsId,
            "dwellTime": self.dwellTime,
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hour": self.hour,
            "minute": self.minute,
            "seconds": self.seconds
        }

    @staticmethod
    def jsonformatList(historyList):
        List=[]
        for item in historyList:
            List.append(History.jsonformat(item))

        return List