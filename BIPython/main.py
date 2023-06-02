from flask import Flask, request
# 创建Flask实例
import settings
from controller.newsController import newsController

from database import db

app = Flask(__name__)
app.config.from_object(settings.Configs)  # 加载flask项目配置
db.init_app(app)

app.register_blueprint(newsController)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/test", methods=['POST', 'GET'])
def test():
    print(request)
    respone = {
        "method ": request.method,
        "body": request.json,
        "head": dict(request.headers),
        "data":  request.args
    }
    return respone

    '''
    {
    "body": {
        "testKey": "testValue"
    },
    "data": {
        "id": "9527",
        "loacl": "Chain"
    },
    "head": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "31",
        "Content-Type": "application/json",
        "Host": "127.0.0.1:5000",
        "Postman-Token": "02854e97-e7a5-444f-a1b8-210283f541e9",
        "User-Agent": "PostmanRuntime/7.32.2"
    },
    "method ": "GET"
}
    '''

if __name__ == "__main__":
    app.run()
