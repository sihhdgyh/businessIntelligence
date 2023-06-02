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
    news=News.query.all()
    return News.jsonformatList(news)

@newsController.route('/getLifeTimeAll', methods=['GET'])
def getLifeTimeAll():
    news=News.query.all()
    return News.jsonformatList(news)

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