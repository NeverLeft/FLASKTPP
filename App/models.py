from werkzeug.security import generate_password_hash, check_password_hash

from App.ModelUtil import BaseModel
from App.ext import db


class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    letter = db.Column(db.String(1), unique=True)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regionName = db.Column(db.String(16))
    cityCode = db.Column(db.Integer, default=0)
    pinYin = db.Column(db.String(64))
    c_letter = db.Column(db.Integer, db.ForeignKey(Letter.id))

    # def __str__(self):
    #     return self.regionName

    # def __unicode__(self):
    #     return self.regionName

    def __repr__(self):
        return self.regionName

"""
insert into movies(id, showname, shownameen, director, leadingRole, type, country, language, duration, screeningmodel,
 openday, backgroundpicture, flag, isdelete) values(228830,"梭哈人生","The Drifting Red Balloon","郑来志",
 "谭佑铭,施予斐,赵韩樱子,孟智超,李林轩","剧情,爱情,喜剧","中国大陆","汉语普通话",90,"4D",date("2018-01-30 00:00:00"),
 "i1/TB19_XCoLDH8KJjy1XcXXcpdXXa_.jpg",1,0);
"""


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    showname = db.Column(db.String(32))
    shownameen = db.Column(db.String(64))
    director = db.Column(db.String(32))
    leadingRole = db.Column(db.String(256))
    type = db.Column(db.String(32))
    country = db.Column(db.String(64))
    language = db.Column(db.String(32))
    duration = db.Column(db.Integer)
    screeningmodel = db.Column(db.String(16))
    openday = db.Column(db.DateTime)
    backgroundpicture = db.Column(db.String(256))
    flag = db.Column(db.Integer)
    isdelete = db.Column(db.Boolean)


"""
insert into cinemas(name,city,district,address,phone,score,hallnum,servicecharge,astrict,flag,isdelete)
 values("深圳戏院影城","深圳","罗湖","罗湖区新园路1号东门步行街西口","0755-82175808",9.7,9,1.2,20,1,0);
"""


class Cinemas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    city = db.Column(db.String(16))
    district = db.Column(db.String(16))
    address = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    score = db.Column(db.Float)
    hallnum = db.Column(db.Integer)
    servicecharge = db.Column(db.Float)
    astrict = db.Column(db.Integer)
    flag = db.Column(db.Integer)
    isdelete = db.Column(db.Boolean)


"""
    文件上传
        1. 原生导流
            - 原生操作
            - 一遍读一遍写
        2. 直接可以save
        3. uploads
"""
PERMISSION_ORDERED = 1
PERMISSION_DELETE = 2
PERMISSION_MODIFCATION = 4


class User(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_name = db.Column(db.String(16), unique=True)
    u_email = db.Column(db.String(64), unique=True)
    u_password = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=False)
    u_permission = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.u_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.u_password, password)

    def check_permission(self, permission):
        return self.u_permission & permission == permission


    # def save(self):
    #     db.session.add(self)
    #     db.session.commit()
    #

# 大厅，  电影院
class Hall(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 1  工字型   12 × 10
    h_type = db.Column(db.Integer)

    h_count = db.Column(db.Integer, default=5)
    # 0 1 2 3 。。。100
    seats = db.Column(db.String(512))


"""
    和大厅和电影的关系
        大厅和电影的关系表
        和购物车一个道理
"""
class MoviePlan(db.Model):

    id = db.Column(db.String(128), primary_key=True)

    mp_movie = db.Column(db.Integer, db.ForeignKey(Movie.id))

    mp_hall = db.Column(db.Integer, db.ForeignKey(Hall.id))

    mp_time = db.Column(db.DateTime)


class Order(BaseModel,db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    o_user = db.Column(db.Integer, db.ForeignKey(User.id))

    o_movie_plan = db.Column(db.String(128), db.ForeignKey(MoviePlan.id))
    # 1 代表已下单，未付款   2 代表已下单已付款 3 ....
    o_status = db.Column(db.Integer, default=1)


class Ticket(BaseModel, db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    t_order = db.Column(db.Integer, db.ForeignKey(Order.id))

    t_seat = db.Column(db.Integer)