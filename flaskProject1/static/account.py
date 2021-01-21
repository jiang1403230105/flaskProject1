#用户管理类
from flask import Blueprint

account=Blueprint('account',__name__)#创建蓝图

@account.route('login',methods=['GET','POST'])
def login():
    pass