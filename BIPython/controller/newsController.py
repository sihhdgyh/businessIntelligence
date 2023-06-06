from datetime import datetime

from flask import Blueprint, request, session
from sqlalchemy import and_, func

from database import db
from entity.history import History
from entity.news import News

newsController = Blueprint('newsController', __name__)




@newsController.route('/getAllNews', methods=['GET'])
def getAllNews():
    news=News.query.all()
    return News.jsonformatList(news)

@newsController.route('/getLifeTime', methods=['GET'])
def getLifeTime():
    newsId=request.args['newsId']
    historys=History.query.filter(History.newsId == newsId)\
        .order_by(History.year.desc())\
        .order_by(History.month.desc()) \
        .order_by(History.day.desc()) \
        .order_by(History.hour.desc()) \
        .order_by(History.minute.desc()) \
        .order_by(History.seconds.desc())\
        .all()
    #History.year.desc(), History.month.desc(),History.day.desc(),History.hour.desc(),History.minute.desc(),History.seconds.desc()
    if len(historys) > 0:
        startHistory = historys[len(historys) - 1]
        start = datetime(year=startHistory.year, month=startHistory.month, day=startHistory.day,
                         hour=startHistory.hour, minute=startHistory.minute, second=startHistory.seconds)

        endHistory = historys[0]
        end = datetime(year=endHistory.year, month=endHistory.month, day=endHistory.day,
                       hour=endHistory.hour, minute=endHistory.minute, second=endHistory.seconds)
        return {
            'start': str(start),
            'end': str(end)
        }
    else:
        return 'error'

@newsController.route('/getLifeTimeAll', methods=['GET'])
def getLifeTimeAll():
    historys = History.query.group_by(History.newsId)\
        .order_by(History.year.desc()) \
        .order_by(History.month.desc()) \
        .order_by(History.day.desc()) \
        .order_by(History.hour.desc()) \
        .order_by(History.minute.desc()) \
        .order_by(History.seconds.desc()) \
        .all()
    return History.jsonformatList(historys)
    # History.year.desc(), History.month.desc(),History.day.desc(),History.hour.desc(),History.minute.desc(),History.seconds.desc()
    # if len(historys) > 0:
    #     startHistory = historys[len(historys) - 1]
    #     start = datetime(year=startHistory.year, month=startHistory.month, day=startHistory.day,
    #                      hour=startHistory.hour, minute=startHistory.minute, second=startHistory.seconds)
    #
    #     endHistory = historys[0]
    #     end = datetime(year=endHistory.year, month=endHistory.month, day=endHistory.day,
    #                    hour=endHistory.hour, minute=endHistory.minute, second=endHistory.seconds)
    #     return {
    #         'start': str(start),
    #         'end': str(end)
    #     }
    # else:
    #     return 'error'

@newsController.route('/newsClickDay', methods=['POST'])
def newsClickDay():
    newsId=request.json['newId']
    year = request.json['year']
    month = request.json['month']
    day = request.json['day']
    clicks= History.query.filter(and_(
        History.newsId == newsId,
        History.year == year,
        History.month == month,
        History.day == day
    )).all()
    return str(len(clicks))


@newsController.route('/categoryClickDay', methods=['POST'])
def categoryClickDay():
    category=request.json['category']
    year = request.json['year']
    month = request.json['month']
    day = request.json['day']

    result=db.session.query(History.id).filter(and_(
        History.newsId==News.newsId,
        News.category == category,
        History.year==year,
        History.month==month,
        History.day==day
    )).all()

    print(result)
    return str(len(result))


@newsController.route('/getUserCategoryClick', methods=['GET'])
def getUserCategoryClick():
    userId=request.args['userId']

    result = db.session.query(News.category,func.count(History.id)).filter(and_(
        History.newsId == News.newsId,
        History.userId == userId
    )).group_by(News.category).all()

    print(result)
    resultJson={}
    for item in result:
        resultJson[item[0]]=item[1]

    return resultJson

@newsController.route('/getCategoryClick', methods=['GET'])
def getCategoryClick():

    result = db.session.query(News.category,func.count(History.id)).filter(and_(
        History.newsId == News.newsId,
    )).group_by(News.category).all()

    print(result)
    resultJson = {}
    for item in result:
        resultJson[item[0]] = item[1]
    return resultJson



'''
根据用户id+天，获取某天该用户对所有种类的新闻的点击量
'''
@newsController.route('/categoryClickUserDay', methods=['POST'])
def categoryClickUserDay():
    userId=request.json['userId']
    year = request.json['year']
    month = request.json['month']
    day = request.json['day']

    result = db.session.query(News.category,func.count(History.id)).filter(and_(
        History.newsId == News.newsId,
        History.year==year,
        History.month==month,
        History.day==day,
        History.userId==userId
    )).group_by(News.category).all()

    print(result)
    resultJson = {}
    for item in result:
        resultJson[item[0]] = item[1]
    return resultJson


'''
按照时间/时间段、新闻主题、新闻标题长度、新闻长度、特定用户、特定多个用户等多种条件和组合进行统计查询
'''
@newsController.route('/multiQuery', methods=['POST'])
def multiQuery():
    year=request.json['year']
    month_min = int(request.json['month_min'])
    day_min = int(request.json['day_min'])
    month_max = int(request.json['month_max'])
    day_max = int(request.json['day_max'])
    category = request.json['category']
    titleLength_min = int(request.json['titleLength_min'])
    newsLength_min = int(request.json['newsLength_min'])
    titleLength_max = int(request.json['titleLength_max'])
    newsLength_max = int(request.json['newsLength_max'])
    userId = request.json['userId']
    result = db.session.query(News).filter(and_(
        History.newsId == News.newsId,
        History.userId==userId,
        History.year==year,
        News.category==category,
        100*History.month+History.day>=100*month_min+day_min,
        100 * History.month + History.day < 100 * month_max + day_max,
        func.char_length(News.headline) >= titleLength_min,
        func.char_length(News.newsBody) >= newsLength_min,
        func.char_length(News.headline) < titleLength_max,
        func.char_length(News.newsBody) < newsLength_max,
    )).all()
    print(result)
    return News.jsonformatList(result)


@newsController.route('/recommendCategory', methods=['GET'])
def recommendCategory():
    result = db.session.query(News.category, func.count(History.id),func.sum(History.dwellTime)).filter(and_(
        History.newsId == News.newsId,
    )).group_by(News.category).order_by((func.count(History.id)+func.sum(History.dwellTime)*0.1).desc()).all()

    print(result)

    return result[0][0]

@newsController.route('/getNewsCA', methods=['POST'])
def getNewsCA():
    category=request.json['category']
    amount = int(request.json['amount'])

    result = News.query.filter(News.category==category).limit(amount).all()

    print(result)

    return News.jsonformatList(result)