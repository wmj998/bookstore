from functools import wraps
from flask import session, redirect, url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        uid = session.get('id')
        manager = session.get('super')
        if uid and manager:
            return func(*args, **kwargs)
        return redirect(url_for('user.login'))
    return wrapper

