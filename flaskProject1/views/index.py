from flask import Flask,Blueprint

index_page=Blueprint('index_page',__name__)#创建蓝图

@index_page.route('/')
def index():
    return "欢迎"