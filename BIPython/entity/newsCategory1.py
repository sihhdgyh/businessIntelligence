from database import db


class NewsCategory(db.Model):
    # 设置表名
    __tablename__ = 'newsCategory'
    # 创建数据库表字段
    # db.Column(类型，约束)
    newsId = db.Column(db.String(200), primary_key=True)
    category = db.Column(db.String(200))

    def jsonformat(self):
        return {
            "newsId": self.newsId,
            "category": self.category,
        }

    @staticmethod
    def jsonformatList(newsCategoryList):
        List=[]
        for item in newsCategoryList:
            List.append(NewsCategory.jsonformat(item))

        return List