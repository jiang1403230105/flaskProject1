#数据库工具类
import pymysql
from flaskProject1.static import constant

# db_con=pymysql.Connection('localhost','root','641641','jyj','utf8')
# db_con=pymysql.connect(host='localhost',user='jyj',password='666666',database='jyj',charset='utf8')
# db_con=pymysql.connect(host=constant.LOCAL_HOST,user=constant.MYSQL_USER,password=constant.MYSQL_PWD,database=constant.DATABASE,charset=constant.ENCODING)
# cursor=db_con.cursor(pymysql.cursors.DictCursor)
# cursor.execute("show databases")
# data=cursor.fetchall()
# print(data)
# cursor.close()
# db_con.close()

#创建数据连接
def create_con():
    db_con=pymysql.connect(host=constant.LOCAL_HOST,user=constant.MYSQL_USER,password=constant.MYSQL_PWD,database=constant.DATABASE,charset=constant.ENCODING)
    cursor=db_con.cursor(pymysql.cursors.DictCursor) #设置游标返回是字典类型
    return db_con,cursor

#关闭数据库链接s
def close_con(con,cursor):
    cursor.close()
    con.close()

#数据库创建表
def create_table():
    con,cursor=create_con()
    class_sql="""create table if not exists class (cid int(11) not null auto_increment,caption varchar (32) not null,primary key (cid))"""

    course_sql="""create table if not exists course(cid int(11) not null  auto_increment,cname varchar (32) not null ,teacher_id int (11),
    primary key (cid),key fk_course_teacher (teacher_id),constraint fk_course_teacher foreign key (teacher_id) references teacher (tid))"""

    student_sql = """create table if not exists student (sid int(11) not null auto_increment,sname varchar(32) not null,
        gender char(1) not null,class_id int (11) not null ,
        primary key (sid),key fk_class (class_id),
        constraint fk_class foreign key (class_id) references class(cid))"""

    teacher_sql = """create table if not exists teacher(tid int(11) not null auto_increment,tname varchar (32) not null,
        primary key (tid))"""

    score_sql="""create table if not exists score(sid int(11) not null auto_increment,student_id int(11) not null,course_id int(11) not null,
     num int (11) not null ,primary key (sid),key fk_score_student (student_id),key fk_score_course (course_id),
     constraint fk_score_student foreign key (student_id) references student(sid),
     constraint  fk_score_course foreign key (course_id) references  course(cid))"""

    cursor.execute(class_sql)
    cursor.execute(student_sql)
    cursor.execute(teacher_sql)
    cursor.execute(course_sql)
    cursor.execute(score_sql)

    data=cursor.fetchall()
    print(data)
    close_con(con,cursor)
# create_table()

def query():
    # 查询“生物”课程比“物理”课程成绩高的所有学生的学号；
    sql1="""select a.student_id,a.cname,a.num,b.cname,b.num from 
    (select score.student_id,course.cname,score.num from score left join course on course.cid=score.course_id where course.cname='生物') as a
    inner join 
    (select score.student_id,course.cname,score.num from score left join course on course.cid=score.course_id where course.cname='物理') as b 
    on a.student_id=b.student_id where a.num>b.num order by a.num desc """
    # 查询平均成绩大于60分的同学的学号和平均成绩；
    sql2="""select b.student_id, student.sname,b.s_avg_num from
    (select student_id,avg(num) as s_avg_num from score group by student_id having s_avg_num>60) as b 
    left join student on student.sid=b.student_id order by s_avg_num desc """
    # 查询所有同学的学号、姓名、选课数、总成绩；
    sql3="""select score.student_id,student.sname,count(score.course_id) as course_num,sum(num) as total_score from score 
    left join student on student.sid=score.student_id group by score.student_id"""
    # 查询姓“李”的老师的个数；
    sql4="""select count(tname) from teacher where tname like '李%'"""
    # 查询没学过“李平”老师课的同学的学号、姓名；
    sql5="""select student.sid,student.sname from student where student.sid not in (select score.student_id from score left join course on course.cid=score.course_id where score.course_id in 
    (select course.cid from course left join teacher on teacher.tid=course.teacher_id where teacher.tname like '李平%')
    group by score.student_id)"""
    con,cursor=create_con()
    cursor.execute(sql5)
    data=cursor.fetchall()
    for item in data:
        print(item)
    close_con(con,cursor)
query()