from sqlalchemy import and_, or_

from models.base import db, User


def register_user(**kwargs):
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()


def login_user(account):
    user = User.query.filter(and_(or_(User.username == account, User.email == account), User.status != 0)).first()
    return user


def query_username(username):
    user = User.query.filter(and_(User.username == username, User.status != 0)).first()
    return user


def query_email(email):
    user = User.query.filter(and_(User.email == email, User.status != 0)).first()
    return user


def query_id(uid):
    user = User.query.get(uid)
    return user


def update_user(uid, **kwargs):
    user = User.query.filter_by(id=uid)
    user.update(kwargs)
    db.session.commit()


def delete_user(uid):
    user = User.query.get(uid)
    user.status = 0
    db.session.commit()

