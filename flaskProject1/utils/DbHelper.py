#数据库工具类
import pymysql

# db_con=pymysql.Connection('localhost','root','123456','pytestdb')
db_con=pymysql.connect('localhost','root','123456','pytestdb')
cursor=db_con.cursor()
cursor.execute("select version()")
data=cursor.fetchone()
cursor.close()
db_con.close()