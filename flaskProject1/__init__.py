from flask import Flask

from flaskProject1.views.account import account
from flaskProject1.views.index import index_page

def create_app():
    app=Flask(__name__)
    app.config.from_object('settings.Config')#加载配置文件

    app.register_blueprint(index_page)#注册蓝图
    app.register_blueprint(account)#注册蓝图
    return app
