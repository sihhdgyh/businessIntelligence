from database import db


class News(db.Model):
    # 设置表名
    __tablename__ = 'news'
    # 创建数据库表字段
    # db.Column(类型，约束)
    newsId = db.Column(db.String(200), primary_key=True)
    category = db.Column(db.String(200))
    topic = db.Column(db.String(200))
    headline = db.Column(db.String(2000))
    newsBody = db.Column(db.String(2000))
    titleEntity = db.Column(db.String(2000))
    entityContent = db.Column(db.String(4000))

    def jsonformat(self):
        return {
            "newsId": self.newsId,
            "category": self.category,
            "topic": self.topic,
            "headline": self.headline,
            "newsBody": self.newsBody,
            "titleEntity": self.titleEntity,
            "entityContent": self.entityContent
        }

    @staticmethod
    def jsonformatList(newsList):
        List=[]
        for item in newsList:
            List.append(News.jsonformat(item))

        return List