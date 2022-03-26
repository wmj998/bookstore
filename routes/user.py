from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import register_user, login_user, query_username, query_email, query_id, update_user, delete_user
from tools.user import login_required

user_bp = Blueprint('user', __name__)


@user_bp.route('/register/', methods=['GET', 'POST'])
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if query_username(username=username):
            error = 'Username is exist!'
            return render_template('user/register.html', email=email, password=password, error=error)
        if query_email(email=email):
            error = 'Email is exist!'
            return render_template('user/register.html', username=username, password=password, error=error)
        else:
            password = generate_password_hash(password)
            register_user(username=username, email=email, password=password)
            return redirect(url_for('.login'))
    return render_template('user/register.html')


@user_bp.route('/login/', methods=['GET', 'POST'])
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        remember = request.form.get('remember')
        user = login_user(account=account)
        if user:
            p_hash = user.password
            if check_password_hash(p_hash, password):
                session['id'] = user.id
                if remember:
                    session.permanent = True
                if user.status == 2:
                    session['super'] = True
                    return redirect(url_for('manager.index'))
                return redirect(url_for('index.index'))
        error = 'Account or Password error'
        return render_template('user/login.html', error=error, account=account, password=password)
    return render_template('user/login.html')


@user_bp.route('/forgot/', methods=['GET', 'POST'])
@user_bp.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        pass
    return render_template('user/forgot.html')


@user_bp.route('/logout/')
@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@user_bp.route('/user/')
@user_bp.route('/user')
@login_required
def show():
    uid = session['id']
    user = query_id(uid)
    return render_template('user/user.html', user=user)


@user_bp.route('/update/<info>/', methods=['GET', 'POST'])
@user_bp.route('/update/<info>', methods=['GET', 'POST'])
@login_required
def update(info):
    if request.method == 'POST':
        uid = session['id']
        value = request.form.get('value')
        if info == 'username':
            if query_username(username=value):
                error = 'Username is exist!'
                return render_template('user/update.html', info=info, error=error)
            update_user(uid=uid, username=value)
        elif info == 'email':
            if query_email(email=value):
                error = 'Email is exist!'
                return render_template('user/update.html', info=info, error=error)
            update_user(uid=uid, email=value)
        elif info == 'password':
            user = query_id(uid)
            p_hash = user.password
            if not check_password_hash(p_hash, value):
                error = 'Password is error!'
                return render_template('user/update.html', info=info, error=error)
            password = request.form.get('password')
            password = generate_password_hash(password)
            update_user(uid=uid, password=password)
            return redirect(url_for('.login'))
        return redirect(url_for('.show'))
    return render_template('user/update.html', info=info)


@user_bp.route('/delete/', methods=['GET', 'POST'])
@user_bp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        password = request.form.get('password')
        uid = session['id']
        user = query_id(uid=uid)
        p_hash = user.password
        if check_password_hash(p_hash, password):
            delete_user(uid=uid)
            logout()
        error = 'Password error!'
        return render_template('user/delete.html', error=error)
    return render_template('user/delete.html')
