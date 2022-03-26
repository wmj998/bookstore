from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash

from models.book import upload_book, add_book, update_book, query_id, upload_state
from models.manager import check_book, show_user, show_book, state_book, search_book, search_user
from models.user import update_user, query_username, query_email
from tools.book import UploadImage
from tools.manager import login_required

manager_bp = Blueprint('manager', __name__, url_prefix='/manager')


@manager_bp.route('')
@login_required
def index():
    return render_template('manager/index.html')


@manager_bp.route('/user/')
@manager_bp.route('/user')
@login_required
def user():
    page = request.args.get('page', 1, int)
    res = show_user(page)
    return render_template('manager/user.html', res=res)


@manager_bp.route('/book/')
@manager_bp.route('/book')
@login_required
def book():
    page = request.args.get('page', 1, int)
    res = show_book(page)
    return render_template('manager/book.html', res=res)


@manager_bp.route('/check/')
@manager_bp.route('/check')
@login_required
def check():
    page = request.args.get('page', 1, int)
    res = check_book(page=page)
    return render_template('manager/check.html', res=res)


@manager_bp.route('/check/<result>/')
@manager_bp.route('/check/<result>')
@login_required
def c_state(result):
    bid = request.args.get('id')
    if result == 'pass':
        state_book(bid=bid, state=1)
    elif result == 'fail':
        state_book(bid=bid, state=2)
    return redirect(url_for('.check'))


@manager_bp.route('/user/<info>/', methods=['GET', 'POST'])
@manager_bp.route('/user/<info>', methods=['GET', 'POST'])
@login_required
def u_update(info):
    uid = request.args.get('id')
    if request.method == 'POST':
        kwargs = request.form.to_dict()
        if info == 'username':
            if query_username(**kwargs):
                error = 'Username is exist!'
                return render_template('manager/u_update.html', info=info, id=uid, error=error)
            update_user(uid=uid, **kwargs)
        elif info == 'email':
            if query_email(**kwargs):
                error = 'Email is exist!'
                return render_template('manager/u_update.html', info=info, id=uid, error=error)
            update_user(uid=uid, **kwargs)
        elif info == 'password':
            password = generate_password_hash(**kwargs)
            update_user(uid=uid, password=password)
        elif info == 'status':
            update_user(uid=uid, **kwargs)
        return redirect(url_for('.user'))
    return render_template('manager/u_update.html', info=info, id=uid)


@manager_bp.route('/book/<info>/', methods=['GET', 'POST'])
@manager_bp.route('/book/<info>', methods=['GET', 'POST'])
@login_required
def b_update(info):
    bid = request.args.get('id')
    if request.method == 'POST':
        kwargs = request.form.to_dict()
        update_book(bid=bid, **kwargs)
        return redirect(url_for('.book'))
    return render_template('manager/b_update.html', info=info, id=bid)


@manager_bp.route('/upload/')
@manager_bp.route('/upload')
@login_required
def upload():
    uid = session['id']
    state = request.args.get('state')
    page = request.args.get('page', 1, int)
    if state:
        res = upload_state(uid=uid, state=state, page=page)
    else:
        res = upload_book(uid=uid, page=page)
    return render_template('manager/upload.html', res=res)


@manager_bp.route('/add/', methods=['GET', 'POST'])
@manager_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        file = request.files.get('file')
        kwargs = request.form.to_dict()
        user_id = session['id']
        image = UploadImage.main(image=file, uid=user_id)
        if not image:
            return render_template('manager/add.html')
        kwargs['state'] = 1
        add_book(image=image, user_id=user_id, **kwargs)
        return redirect(url_for('.upload'))
    return render_template('manager/add.html')


@manager_bp.route('/product/')
@manager_bp.route('/product')
@login_required
def product():
    page = request.args.get('page')
    bid = request.args.get('id')
    res = query_id(bid=bid)
    return render_template('manager/product.html', book=res, page=page)


@manager_bp.route('/finish/')
@manager_bp.route('/finish')
@login_required
def finish():
    bid = request.args.get('id')
    state_book(bid=bid, state=3)
    return redirect(url_for('.upload'))


@manager_bp.route('/delete/')
@manager_bp.route('/delete')
@login_required
def delete():
    bid = request.args.get('id')
    state_book(bid=bid, state=4)
    return redirect(url_for('.upload'))


@manager_bp.route('/update/', methods=['GET', 'POST'])
@manager_bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    bid = request.args.get('id')
    if request.method == 'POST':
        file = request.files.get('file')
        kwargs = request.form.to_dict()
        user_id = session['id']
        image = UploadImage.main(image=file, uid=user_id)
        if not image:
            return render_template('manager/update.html')
        update_book(bid=bid, image=image, user_id=user_id, **kwargs)
        return redirect(url_for('.upload'))
    page = request.args.get('page')
    return render_template('manager/update.html', id=bid, page=page)


@manager_bp.route('/book/search/')
@manager_bp.route('/book/search')
@login_required
def b_search():
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, int)
    res = search_book(keyword=keyword, page=page)
    return render_template('manager/book.html', res=res, keyword=keyword)


@manager_bp.route('/user/search/')
@manager_bp.route('/user/search')
@login_required
def u_search():
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, int)
    res = search_user(keyword=keyword, page=page)
    return render_template('manager/user.html', res=res, keyword=keyword)
