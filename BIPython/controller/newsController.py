import time
from datetime import datetime, date

from flask import Blueprint, request, session
from sqlalchemy import and_, func, extract, or_

from database import db, fp
from entity.categoryDayClick import categoryDayClick
from entity.history import History
from entity.news import News
from entity.newsCategory1 import NewsCategory
from entity.newsCategoryHistory1 import newsCategoryHistory

newsController = Blueprint('newsController', __name__)





@newsController.route('/test', methods=['POST'])
def getAllNews1():
    category = request.json['category']
    year = request.json['year']
    month = request.json['month']
    day = request.json['day']
    print(db.session.query(
        func.count(History.id)
    ).filter(
        News.category==category,
        News.newsId==History.newsId,
        extract('year', History.exposureTime) == year,
        extract('month', History.exposureTime) == month,
        extract('day', History.exposureTime) == day,
    ))
    # userId = History.query.filter(and_(
    #     History.id==13723424
    #      )).limit(1).all()
    return "History.jsonformatList(userId)"


@newsController.route('/getAllNews', methods=['GET'])
def getAllNews():
    news=News.query.all()
    return News.jsonformatList(news)

@newsController.route('/getLifeTime', methods=['GET'])
def getLifeTime():
    newsId=request.args['newsId']
    time1 = time.time()
    date1=datetime.now()
    historysQuery=History.query.filter(History.newsId == newsId)\
        .order_by(History.exposureTime.desc())
    historys=historysQuery.all()
    time2 = time.time()
    date2 = datetime.now()
    fp.write(str(historysQuery) + ',' + str(date1) + ',' + str(date2) + "," + str(time2 - time1) + '\n')
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
    date1=datetime.now()
    clicksQuery= db.session.query(func.count(History.id)).filter(and_(
        History.newsId == newsId,
        extract('year', History.exposureTime) == year,
        extract('month', History.exposureTime) == month,
        extract('day', History.exposureTime) == day,
    ))
    clicks=clicksQuery.all()
    time2 = time.time()
    date2=datetime.now()
    fp.write(str(clicksQuery) + ',' + str(date1) + ',' + str(date2) + "," + str(time2 - time1) + '\n')
    print("查询时间：" + str(time2 - time1))
    return str(clicks[0][0])


@newsController.route('/categoryClickDay', methods=['POST'])
def categoryClickDay():
    category=request.json['category']
    year = request.json['year']
    month = request.json['month']
    day = request.json['day']
    timemin=date(year=year,month=month,day=day)
    time1 = time.time()
    date1=datetime.now()
    resultQuery=db.session.query(func.sum(categoryDayClick.amount)).filter(and_(
        categoryDayClick.category==category,
        categoryDayClick.exposureTime==timemin,

    ))
    result=resultQuery.all()
    time2 = time.time()
    date2=datetime.now()
    fp.write(str(resultQuery) + ',' + str(date1) + ',' + str(date2) + "," + str(time2 - time1) + '\n')
    print("查询时间：" + str(time2 - time1))
    print(result)
    return str(result[0][0])


@newsController.route('/getUserCategoryClick', methods=['GET'])
def getUserCategoryClick():
    userId=request.args['userId']
    date1=datetime.now()
    time1 = time.time()
    resultQuery = db.session.query(News.category,History.exposureTime,func.count(History.id)).filter(and_(
        History.newsId == News.newsId,
        History.userId == userId
    )).group_by(News.category,History.exposureTime)
    result=resultQuery.all()
    time2 = time.time()
    date2=datetime.now()
    fp.write(str(resultQuery) + ',' + str(date1) + ',' + str(date2) + "," + str(time2 - time1) + '\n')
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
    date1=datetime.now()
    time1 = time.time()
    resultQuery = categoryDayClick.query
    result=resultQuery.all()
    time2 = time.time()
    date2=datetime.now()
    fp.write(str(resultQuery) + ',' + str(date1) + ',' + str(date2) + "," + str(time2 - time1) + '\n')
    print("查询时间：" + str(time2 - time1))
    print(result)
    resultJson = {}
    category=[]
    for item in result:
        if item.category in resultJson.keys():

            #print(type(resultJson[item[0]]))
            resultJson[item.category].append({
                "time": str(item.exposureTime),
                "amount": str(item.amount)
            })
        else:
            resultJson[item.category]=[{
                "time": str(item.exposureTime),
                "amount": str(item.amount)
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
    date1=datetime.now()
    time1 = time.time()
    resultQuery = db.session.query(News.category,func.count(History.id)).filter(and_(
        History.userId == userId,
        History.newsId == News.newsId,
        extract('year', History.exposureTime) == year,
        extract('month', History.exposureTime) == month,
        extract('day', History.exposureTime) == day,
    )).group_by(News.category)
    result=resultQuery.all()
    time2 = time.time()
    date2=datetime.now()
    fp.write(str(resultQuery) + ',' + str(date1) + ',' + str(date2) + "," + str(time2 - time1) + '\n')
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
    start_time=request.json['start_time']
    end_time = request.json['end_time']
    category = request.json['category']
    time_min=datetime.strptime(start_time, '%Y-%m-%d')
    time_max = datetime.strptime(end_time, '%Y-%m-%d')
    print(time_min)
    # time_min=datetime(year=year,month=month_min,day=day_min,hour=0,minute=0,second=0)
    # time_max=datetime(year=year,month=month_max,day=day_max,hour=0,minute=0,second=0)
    titleLength_max = int(request.json['titleLength_max'])
    newsLength_max = int(request.json['newsLength_max'])
    userId = request.json['userId']
    date1=datetime.now()
    time1 = time.time()
    if userId=='':
        resultQuery = db.session.query(News).filter(and_(
            # result = History.query.filter(and_(
            History.newsId == News.newsId,
            #History.userId == userId,
            News.category == category,
            History.exposureTime >= time_min,
            History.exposureTime < time_max,
            # 100*History.month+History.day>=100*month_min+day_min,
            # 100 * History.month + History.day < 100 * month_max + day_max,
            func.char_length(News.headline) < titleLength_max,
            func.char_length(News.newsBody) < newsLength_max,
        ))

    else:
        resultQuery = db.session.query(News).filter(and_(
            # result = History.query.filter(and_(
            History.userId == userId,
            History.newsId == News.newsId,

            News.category == category,
            History.exposureTime >= time_min,
            History.exposureTime < time_max,
            # 100*History.month+History.day>=100*month_min+day_min,
            # 100 * History.month + History.day < 100 * month_max + day_max,
            func.char_length(News.headline) < titleLength_max,
            func.char_length(News.newsBody) < newsLength_max,
        ))


    result=resultQuery.limit(amount).all()
    #result = resultQuery
    time2 = time.time()
    date2=datetime.now()
    fp.write(str(resultQuery) + ',' + str(date1) + ',' + str(date2) + "," + str(time2 - time1) + '\n')
    print('查询时间：'+str(time2-time1))
    print("result")
    print(result)
    return News.jsonformatList(result)


@newsController.route('/recommendCategory', methods=['GET'])
def recommendCategory():
    time1 = time.time()
    date1=datetime.now()
    resultQuery = db.session.query(categoryDayClick.category, func.sum(categoryDayClick.amount),func.sum(categoryDayClick.totalTime)).group_by(categoryDayClick.category).order_by((func.sum(categoryDayClick.amount)+func.sum(categoryDayClick.totalTime)*0.1).desc())
    result=resultQuery.all()
    time2 = time.time()
    date2 = datetime.now()
    fp.write(str(resultQuery)+','+str(date1)+','+str(date2)+ ","+str(time2 - time1)+'\n')
    print("查询时间：" + str(time2 - time1))
    print(result)

    return result[0][0]

@newsController.route('/getNewsCA', methods=['POST'])
def getNewsCA():
    category=request.json['category']
    amount = int(request.json['amount'])
    date1=datetime.now()
    time1 = time.time()
    resultQuery = News.query.filter(News.category==category).limit(amount)
    result=resultQuery.all()
    time2 = time.time()
    date2=datetime.now()
    fp.write(str(resultQuery) + ',' + str(date1) + ',' + str(date2) + "," + str(time2 - time1) + '\n')
    print("查询时间：" + str(time2 - time1))
    print(result)

    return News.jsonformatList(result)