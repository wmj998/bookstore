import datetime

from flask_sqlalchemy import SQLAlchemy

from app import app

db = SQLAlchemy(app)


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, comment='ID')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')


class User(Base):
    __tablename__ = 'user'
    username = db.Column(db.String(255), comment='用户名', index=True)
    email = db.Column(db.String(255), comment='邮箱', index=True)
    password = db.Column(db.String(255), comment='密码')
    status = db.Column(db.Integer, default=1, comment='状态: {0: delete, 1: normal, 2: manager}', index=True)
    book = db.relationship('Book', backref='user', lazy='dynamic')
    cart = db.relationship('Cart', backref='user', lazy='dynamic')


class Book(Base):
    __tablename__ = 'book'
    image = db.Column(db.String(255), comment='图片路径')
    name = db.Column(db.String(255), comment='书名', index=True)
    author = db.Column(db.String(255), comment='作者', index=True)
    number = db.Column(db.Integer, comment='数量')
    price = db.Column(db.DECIMAL(10, 2), comment='价格')
    type = db.Column(db.String(255), comment='类型', index=True)
    description = db.Column(db.Text, comment='描述')
    state = db.Column(db.Integer, default=0, comment='状态: {0: wait, 1: pass, 2: fail, 3: finish, 4: delete}', index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), comment='添加用户ID')
    cart = db.relationship('Cart', backref='book', lazy='dynamic')


class Cart(Base):
    __tablename__ = 'cart'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), comment='用户ID')
    book_id = db.Column(db.Integer, db.ForeignKey(Book.id), comment='图书ID')
    number = db.Column(db.Integer, default=1, comment='数量')
    state = db.Column(db.Integer, default=1, comment='状态: {0: delete, 1: normal}', index=True)


db.create_all()
