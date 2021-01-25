#数据库工具类
import pymysql

# db_con=pymysql.Connection('localhost','root','123456','pytestdb')
db_con=pymysql.connect(host='localhost',user='root',password='123456',database='pytestdb',charset='utf8')
cursor=db_con.cursor()
cursor.execute("select version()")
data=cursor.fetchone()
cursor.close()
db_con.close()

#创建数据连接
def create_con():
    pass

#关闭数据库
def close_con():
    pass