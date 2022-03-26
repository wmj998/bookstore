from sqlalchemy import and_, or_

from models.base import db, Book


def query_id(bid):
    book = Book.query.get(bid)
    return book


def search_book(keyword, page, size=8):
    book = Book.query.filter(and_(or_(Book.name == keyword, Book.author == keyword, Book.type == keyword), Book.state == 1)).order_by(-Book.id).paginate(page, size)
    return book


def upload_book(uid, page, size=8):
    book = Book.query.filter(and_(Book.user_id == uid, Book.state != 4)).order_by(-Book.id).paginate(page, size)
    return book


def upload_state(uid, state, page, size=8):
    book = Book.query.filter_by(user_id=uid, state=state).order_by(-Book.id).paginate(page, size)
    return book


def add_book(**kwargs):
    book = Book(**kwargs)
    db.session.add(book)
    db.session.commit()


def update_book(bid, **kwargs):
    book = Book.query.filter_by(id=bid)
    book.update(kwargs)
    db.session.commit()


def state_book(uid, bid, state):
    try:
        book = Book.query.filter_by(id=bid, user_id=uid).first()
        book.state = state
        db.session.commit()
    except Exception as e:
        print(e)


def index_book():
    book = Book.query.limit(4).all()
    return book
