from flask import Flask

from .static import account

def create_app():
    app=Flask(__name__)
    app.config.from_object('settings.Config')#加载配置文件
    app.register_blueprint(account)#注册蓝图
    return app
