
''' 建库:AID1811db  建表:suinfo '''
import pymysql
import warnings

#数据库连接对象
db = pymysql.connect(
    'localhost',
    'root',
    '123456',
    charset='utf8')

#游标对象
cursor = db.cursor()

#执行sql命令
# c_db = 'create database AID1811db charset utf8'
u_db = 'use AID1811db'
# c_tab = 'create table stuinfo(name varchar(20))'
ins = 'insert into stuinfo values("Tom")'

#忽略警告
warnings.filterwarnings('ignore')

# cursor.execute(c_db)
cursor.execute(u_db)
# cursor.execute(c_tab)
cursor.execute(ins)

#另外一种execute传参方式
a = 'tom'
cursor.execute('insert into stuinfo values(%s)',a)

#以字典方式给前面传参再存入
b = {
    'name':'toney'
}
cursor.execute('insert into stuinfo values(%(name)s)',b)

#提交到数据库执行
db.commit()

#关闭
cursor.close()
db.close()



