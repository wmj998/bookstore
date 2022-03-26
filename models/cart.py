from sqlalchemy import and_, or_

from models.base import db, Cart


def add_cart(uid, bid):
    cart = Cart(user_id=uid, book_id=bid)
    db.session.add(cart)
    db.session.commit()


def query_cart(uid, bid):
    cart = Cart.query.filter_by(user_id=uid, book_id=bid, state=1).first()
    return cart


def query_uid(uid):
    cart = Cart.query.filter_by(user_id=uid, state=1).order_by(-Cart.id).all()
    return cart


def delete_cart(cid):
    cart = Cart.query.get(cid)
    cart.state = 0
    db.session.commit()


def update_cart(cid, number):
    cart = Cart.query.get(cid)
    cart.number = number
    db.session.commit()


def add_number(cid):
    cart = Cart.query.get(cid)
    cart.number += 1
    db.session.commit()
