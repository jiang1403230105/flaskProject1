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
    # 查询学过“001”并且也学过编号“002”课程的同学的学号、姓名；
    sql6="""select b.sid,b.sname from (select score.course_id,student.sid,student.sname from score 
    left join student on student.sid=score.student_id where score.course_id between 1 and 2) as b group by b.sid """
    # 查询学过“叶平”老师所教的所有课的同学的学号、姓名；
    sql7="""select student.sid,student.sname from score left join student on student.sid=score.student_id where score.course_id in 
    (select course.cid from course left join teacher on teacher.tid=course.teacher_id where teacher.tname like '李平%') group by student.sid 
    having count(student_id)=2"""
    # 查询课程编号“002”的成绩比课程编号“001”课程低的所有同学的学号、姓名；
    sql8="""select a.sid,a.sname,a.num as score_2,b.num as score_1 from 
    (select student.sid,student.sname,score.num from score left join student on student.sid=score.student_id where score.course_id=2) as a
    inner join 
    (select student.sid,student.sname,score.num from score left join student on student.sid=score.student_id where score.course_id=1) as b
    on a.sid=b.sid where a.num<b.num"""
    # 查询有课程成绩小于60分的同学的学号、姓名；
    sql9="""select sid,sname from student where sid in (select score.student_id from score where score.num>60 group by score.student_id)"""
    # 查询没有学全所有课的同学的学号、姓名；
    sql10="""select sid, sname from student where sid in 
    (select student_id from score group by student_id having count(course_id)!=(select count(cid) from course)"""
    # 查询至少有一门课与学号为“001”的同学所学相同的同学的学号和姓名；
    sql11="""select sid,sname from student where sid in 
    (select score.student_id from score where course_id in 
    (select score.course_id from score where student_id=1)
    and student_id!=1 group by student_id)"""
    # 查询和“002”号的同学学习的课程完全相同的其他同学学号和姓名；
    sql12="""select sid,sname from student where sid in 
    (select score.student_id from score where course_id in 
    (select score.course_id from score where score.student_id=1)
    and student_id !=1 group by student_id
    having count(1)=(select count(score.course_id) from score where student_id=1))"""
    # 向SC表中插入一些记录，这些记录要求符合以下条件：①没有上过编号“002”课程的同学学号；②插入“002”号课程的平均成绩；
    sql13="""insert into score(student_id,course_id,num) select student_id ,2,(select avg(num) from score where course_id =2) from score where course_id!=2 group by student_id"""
    # 按平均成绩从低到高显示所有学生的“语文”、“数学”、“英语”三门的课程成绩，按如下形式显示： 学生ID, 语文, 数学, 英语, 有效课程数, 有效平均分；
    sql14="""select student_id as 学号,
    ---(select num from score left join course on course.cid=score.course_id where course.cname='生物' and student_id = s1.student_id)as 生物,---
    ---(select num from score left join course on course.cid=score.course_id where course.cname='物理' and student_id = s1.student_id)as 物理,---
    (select num from score left join course on course.cid=score.course_id where course.cname='美术' and student_id = s1.student_id)as 美术
    from score as s1 group by student_id"""
    # 查询各科成绩最高和最低的分：以如下形式显示：课程ID，最高分，最低分；
    sql15="""select score.course_id as 课程id,course.cname as 课程名称,max(score.num) as 最高分,min(score.num) as 最低分
    from score left join course on score.course_id=course.cid group by course_id"""
    # 按各科平均成绩从低到高和及格率的百分数从高到低顺序；
    sql16="""select course_id,course.cname,avg(score.num) as avg_num from score left join course on score.course_id=course.cid group by score.course_id order by avg_num desc """
    sql17="""select a.cid,a.cname,concat(round(b.s/a.ss*100,1),'%') as 及格率 from 
    (select course.cid,course.cname,count(score.course_id) as ss from score left join course on course.cid=score.course_id group by course_id)as a 
    inner join 
    (select course_id,count(num)as s from score where score.num>60 group by course_id) as b 
    on a.cid=b.course_id order by 及格率 desc """
    sql18="""select course.cname,teacher.tname,xxx.avg_score from course 
    left join teacher on teacher.tid=course.teacher_id
    left join (select course_id,avg(num) as avg_score from score group by course_id)as xxx on xxx.course_id=course.cid
    order by xxx.avg_score desc """
    # 查询各科成绩前三名的记录: (不考虑成绩并列情况)
    sql19="""select cid as 课程号,cname as 课程名称,
    (select num from score as s2 where s1.cid=s2.course_id group by num order by num desc limit 0,1)as 第一,
    (select num from score as s2 where s1.cid=s2.course_id group by num order by num desc limit 1,1)as 第二,
    (select num from score as s2 where s1.cid=s2.course_id group by num order by num desc limit 2,1)as 第三
    from course as s1"""
    # 查询每门课程被选修的学生数；
    sql20="""select course.cid as 课程号, course.cname as 课程名称,count(1) as 选修人数 from score left join course on course.cid=score.course_id group by score.course_id"""
    # 查询出只选修了6门课程的全部学生的学号和姓名；
    sql21="""select student.sid,student.sname from student where student.sid in 
    (select score.student_id from score group by score.student_id having count(1)=6)"""
    # 查询男生、女生的人数；
    sql22="""select gender,count(1) as 人数 from student group by gender"""
    # 查询姓“张”的学生名单；
    sql23="""select * from student where sname like '张%'"""
    sql24="""select sname,count(1) from student group by sname"""
    # 查询每门课程的平均成绩，结果按平均成绩升序排列，平均成绩相同时，按课程号降序排列；
    sql25="""select course.cid as 课程号,course.cname as 课程名称 ,avg(score.num) as 平均分 from score 
    left join course on course.cid=score.course_id group by score.course_id order by 平均分 asc ,课程名称 desc """
    # 查询平均成绩大于85的所有学生的学号、姓名和平均成绩；
    sql26="""select student.sid,student.sname,avg(score.num) as 平均分 from score 
    left join student on student.sid=score.student_id group by score.student_id having 平均分>85"""
    # 查询课程名称为“数学”，且分数低于60的学生姓名和分数；
    sql27="""select student.sname,score.num from score 
    left join course on  course.cid=score.course_id 
    left join student on student.sid=score.student_id where course.cname='物理' and score.num<60"""
    # 查询课程编号为003且课程成绩在80分以上的学生的学号和姓名；
    sql28="""select student.sid,student.sname,num from student left join score on score.student_id=student.sid where score.num>80 and score.course_id"""
    sql29="""select count(distinct student_id) as 选课的总人数 from score """
    # 查询选修“杨艳”老师(这个老师没有，就以张磊老师举例)所授课程的学生中，成绩最高的学生姓名及其成绩；
    sql30="""select student.sid,student.sname,course.cname,max(score.num) from score 
    left join course on course.cid=score.course_id
    left join student on student.sid=score.student_id 
    left join teacher on teacher.tid=course.teacher_id 
    where teacher.tname like '刘海燕老师' order by num"""
    # 查询各个课程及相应的选修人数；
    sql31="""select course.cname as 课程,count(distinct score.student_id) as 选修人数 from course left join score on score.course_id=course.cid group by score.course_id"""
    # 查询每门课程成绩最好的前两名；
    sql32="""select course.cid as 课程号,course.cname as 课程名称,
    (select num from score where score.course_id=course.cid group by num order by num desc limit 0,1) as 第一,
    (select num from score where score.course_id=course.cid group by num order by num desc limit 1,1) as 第二 from course """
    # 检索至少选修两门课程的学生学号；
    sql33="""select student_id from score group by student_id having count(1)>1"""
    sql34="""select course_id as 课程号,course.cname as 课程名称, count(distinct student_id) as 选课的学生数 from score
     left join course on course.cid=score.course_id group by score.course_id """
    # 查询没学过“李平”老师讲授的任一门课程的学生姓名；
    sql35="""select student.sid,student.sname from student where student.sid not in 
    (select score.student_id from score where score.course_id in 
    (select course.cid from course left join teacher on teacher.tid=course.teacher_id where tname='李平老师') group by student_id)"""
    # 查询两门以上不及格课程的同学的学号及其平均成绩；
    sql36="""select student.sid as 学号,student.sname as 姓名 , avg(score.num) as 平均成绩 from score 
    left join student on student.sid=score.student_id 
    where score.student_id in (select score.student_id from score where num<60 group by score.student_id having count(1)>1)
    group by score.student_id"""
    # 检索“004”课程分数小于60，按分数降序排列的同学学号；
    sql37="""select student_id,num from score where course_id=4 and num <60 order by num asc """
    con,cursor=create_con()
    cursor.execute(sql37)
    data=cursor.fetchall()
    for item in data:
        print(item)
    close_con(con,cursor)
query()