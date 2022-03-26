from sqlalchemy import or_

from models.base import db, Book, User


def check_book(page, size=10):
    book = Book.query.filter_by(state=0).paginate(page, size)
    return book


def show_user(page, size=10):
    user = User.query.order_by(-User.id).paginate(page, size)
    return user


def show_book(page, size=10):
    book = Book.query.order_by(-Book.id).paginate(page, size)
    return book


def state_book(bid, state):
    try:
        book = Book.query.get(bid)
        book.state = state
        db.session.commit()
    except Exception as e:
        print(e)


def search_book(keyword, page, size=10):
    book = Book.query.filter(or_(Book.id == keyword, Book.name == keyword, Book.author == keyword)).order_by(-Book.id).paginate(page, size)
    return book


def search_user(keyword, page, size=10):
    user = User.query.filter(or_(User.id == keyword, User.username == keyword, User.email == keyword)).order_by(-User.id).paginate(page, size)
    return user

