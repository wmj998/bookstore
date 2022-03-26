from flask import session, redirect, url_for
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        uid = session.get('id')
        if uid:
            return func(*args, **kwargs)
        return redirect(url_for('user.login'))
    return wrapper

