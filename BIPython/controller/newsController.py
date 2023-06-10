import time
from datetime import datetime

from flask import Blueprint, request, session
from sqlalchemy import and_, func, extract, or_

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
    time1 = time.time()
    historys=History.query.filter(History.newsId == newsId)\
        .order_by(History.exposureTime.desc())\
        .all()
    time2 = time.time()
    print("查询时间："+str(time2-time1))
    #History.year.desc(), History.month.desc(),History.day.desc(),History.hour.desc(),History.minute.desc(),History.seconds.desc()
    if len(historys) > 0:
        start = historys[len(historys) - 1].exposureTime

        end = historys[0].exposureTime

        return {
            'start': str(start),
            'end': str(end)
        }
    else:
        return 'error'

@newsController.route('/getLifeTimeAll', methods=['GET'])
def getLifeTimeAll():
    historys = History.query.group_by(History.newsId)\
        .order_by(History.exposureTime.desc()) \
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
    time1 = time.time()

    clicks= History.query.filter(and_(
        History.newsId == newsId,
        extract('year', History.exposureTime) == year,
        extract('month', History.exposureTime) == month,
        extract('day', History.exposureTime) == day,
    )).all()
    time2 = time.time()
    print("查询时间：" + str(time2 - time1))
    return str(len(clicks))


@newsController.route('/categoryClickDay', methods=['POST'])
def categoryClickDay():
    category=request.json['category']
    year = request.json['year']
    month = request.json['month']
    day = request.json['day']
    time1 = time.time()
    result=db.session.query(func.count(History.id)).filter(and_(
        History.newsId==News.newsId,
        News.category == category,
        extract('year', History.exposureTime) == year,
        extract('month', History.exposureTime) == month,
        extract('day', History.exposureTime) == day,
    )).all()
    time2 = time.time()
    print("查询时间：" + str(time2 - time1))
    print(result)
    return str(result[0][0])


@newsController.route('/getUserCategoryClick', methods=['GET'])
def getUserCategoryClick():
    userId=request.args['userId']

    time1 = time.time()
    result = db.session.query(News.category,History.exposureTime,func.count(History.id)).filter(and_(
        History.newsId == News.newsId,
        History.userId == userId
    )).group_by(News.category,History.exposureTime).all()
    time2 = time.time()
    print("查询时间：" + str(time2 - time1))
    print(result)
    resultJson=[]
    for item in result:
        resultJson.append({
            item[0]:{
                "time": str(item[1]),
                "amount": str(item[2])
            },
            # "category":item[0],
            # "time":str(item[1]),
            # "amount":str(item[2])
        })

    return resultJson

@newsController.route('/getCategoryClick', methods=['GET'])
def getCategoryClick():
    time1 = time.time()
    result = db.session.query(News.category,History.exposureTime,func.count(History.id)).filter(and_(
        History.newsId == News.newsId,
    )).group_by(News.category,History.exposureTime).all()
    time2 = time.time()
    print("查询时间：" + str(time2 - time1))
    print(result)
    resultJson = {}
    category=[]
    for item in result:
        if item[0] in resultJson.keys():

            #print(type(resultJson[item[0]]))
            resultJson[item[0]].append({
                "time": str(item[1]),
                "amount": str(item[2])
            })
        else:
            resultJson[item[0]]=[{
                "time": str(item[1]),
                "amount": str(item[2])
            }]
    resultList=[]
    for item in resultJson.keys():
        resultList.append({
            item:resultJson[item]
        })
    return resultList



'''
根据用户id+天，获取某天该用户对所有种类的新闻的点击量
'''
@newsController.route('/categoryClickUserDay', methods=['POST'])
def categoryClickUserDay():
    userId=request.json['userId']
    year = request.json['year']
    month = request.json['month']
    day = request.json['day']

    time1 = time.time()
    result = db.session.query(News.category,func.count(History.id)).filter(and_(
        History.userId == userId,
        History.newsId == News.newsId,
        extract('year', History.exposureTime) == year,
        extract('month', History.exposureTime) == month,
        extract('day', History.exposureTime) == day,
    )).group_by(News.category).all()
    time2 = time.time()
    print("查询时间：" + str(time2 - time1))
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
    amount = int(request.json['amount'])
    year=int(request.json['year'])
    month_min = int(request.json['month_min'])
    day_min = int(request.json['day_min'])
    month_max = int(request.json['month_max'])
    day_max = int(request.json['day_max'])
    category = request.json['category']
    print(category)
    time_min=datetime(year=year,month=month_min,day=day_min,hour=0,minute=0,second=0)
    time_max=datetime(year=year,month=month_max,day=day_max,hour=0,minute=0,second=0)
    titleLength_min = int(request.json['titleLength_min'])
    newsLength_min = int(request.json['newsLength_min'])
    titleLength_max = int(request.json['titleLength_max'])
    newsLength_max = int(request.json['newsLength_max'])
    userId = request.json['userId']
    time1 = time.time()
    #resultQuery="db.session.query(News).filter(and_(History.newsId == News.newsId,"
    #for item in category:

    # sql = "SELECT news.newsId AS news_newsId, " \
    #       "news.category AS news_category, " \
    #       "news.topic AS news_topic, " \
    #       "news.headline AS news_headline, " \
    #       "news.newsBody AS news_newsBody" \
    #       " FROM news, history" \
    #       " WHERE account_stocks.stock_code = stocks.stock_code " \
    #       "and account_stocks.account = :account_1"
    # #  返回的是rawProxy对象，还需要转为前端可以接受的Dict
    # stock_list = db.session.execute(sql, {'account_1': account1})
    # list1 = list(stock_list)
    # ret_list = []
    # for stock in list1:
    #     list1 = {'id': stock[0],
    #              'account': stock[1],
    #              'stock_code': stock[2],
    #              'number': float(stock[3]),
    #              'cost': float(stock[4]),
    #              'stock_name': stock[5],
    #              'current_price': float(stock[6])
    #              }
    #     ret_list.append(list1)
    # print(ret_list)
    # stock_list = AccountStock.query.filter(
    #     AccountStock.account == account1).all()

    if userId=='':
        resultQuery = db.session.query(News).filter(and_(
            # result = History.query.filter(and_(
            History.newsId == News.newsId,
            #History.userId == userId,
            #News.category == category,
            History.exposureTime >= time_min,
            History.exposureTime < time_max,
            # 100*History.month+History.day>=100*month_min+day_min,
            # 100 * History.month + History.day < 100 * month_max + day_max,
            func.char_length(News.headline) >= titleLength_min,
            func.char_length(News.newsBody) >= newsLength_min,
            func.char_length(News.headline) < titleLength_max,
            func.char_length(News.newsBody) < newsLength_max,
        ))

    else:
        resultQuery = db.session.query(News).filter(and_(
            # result = History.query.filter(and_(
            History.newsId == News.newsId,
            History.userId == userId,
            #News.category == category,
            History.exposureTime >= time_min,
            History.exposureTime < time_max,
            # 100*History.month+History.day>=100*month_min+day_min,
            # 100 * History.month + History.day < 100 * month_max + day_max,
            func.char_length(News.headline) >= titleLength_min,
            func.char_length(News.newsBody) >= newsLength_min,
            func.char_length(News.headline) < titleLength_max,
            func.char_length(News.newsBody) < newsLength_max,
        ))

    # for item in category:
    #     resultQuery = resultQuery.filter(or_(
    #         News.category == item
    #     ))
    # resultQuery = resultQuery.filter(or_(
    #     News.category == category[0],
    #     News.category == category[1],
    # ))
    result=resultQuery.limit(amount).all()
    #result = resultQuery
    time2 = time.time()
    print(time2-time1)
    print("result")
    print(result)
    #return News.jsonformatList(result)
    return News.jsonformatList(result)


@newsController.route('/recommendCategory', methods=['GET'])
def recommendCategory():
    time1 = time.time()
    result = db.session.query(News.category, func.count(History.id),func.sum(History.dwellTime)).filter(and_(
        History.newsId == News.newsId,
    )).group_by(News.category).order_by((func.count(History.id)+func.sum(History.dwellTime)*0.1).desc()).all()
    time2 = time.time()
    print("查询时间：" + str(time2 - time1))
    print(result)

    return result[0][0]

@newsController.route('/getNewsCA', methods=['POST'])
def getNewsCA():
    category=request.json['category']
    amount = int(request.json['amount'])
    time1 = time.time()
    result = News.query.filter(News.category==category).limit(amount).all()
    time2 = time.time()
    print("查询时间：" + str(time2 - time1))
    print(result)

    return News.jsonformatList(result)