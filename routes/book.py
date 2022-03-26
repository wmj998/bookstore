from flask import Blueprint, render_template, request, redirect, url_for, session

from models.book import search_book, add_book, state_book, upload_book, query_id, update_book, upload_state
from tools.book import UploadImage
from tools.user import login_required

book_bp = Blueprint('book', __name__, url_prefix='/book')


@book_bp.route('/info/')
@book_bp.route('/info')
@login_required
def info():
    bid = request.args.get('id')
    book = query_id(bid=bid)
    return render_template('book/info.html', book=book)


@book_bp.route('/search/')
@book_bp.route('/search')
@login_required
def search():
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, int)
    res = search_book(keyword=keyword, page=page)
    return render_template('book/search.html', res=res, keyword=keyword, page=page)


@book_bp.route('/detail/')
@book_bp.route('/detail')
@login_required
def detail():
    bid = request.args.get('id')
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, int)
    book = query_id(bid=bid)
    return render_template('book/detail.html', book=book, keyword=keyword, page=page)


@book_bp.route('/add/', methods=['GET', 'POST'])
@book_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        file = request.files.get('file')
        kwargs = request.form.to_dict()
        user_id = session['id']
        image = UploadImage.main(image=file, uid=user_id)
        if not image:
            return render_template('book/add.html')
        add_book(image=image, user_id=user_id, **kwargs)
        return redirect(url_for('.upload'))
    return render_template('book/add.html')


@book_bp.route('/upload/')
@book_bp.route('/upload')
@login_required
def upload():
    page = request.args.get('page', 1, int)
    uid = session['id']
    state = request.args.get('state')
    if state:
        res = upload_state(uid=uid, state=state, page=page)
    else:
        res = upload_book(uid=uid, page=page)
    return render_template('book/upload.html', res=res)


@book_bp.route('/product/')
@book_bp.route('/product')
@login_required
def product():
    page = request.args.get('page')
    bid = request.args.get('id')
    book = query_id(bid=bid)
    return render_template('book/product.html', book=book, page=page)


@book_bp.route('/update/', methods=['GET', 'POST'])
@book_bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    bid = request.args.get('id')
    if request.method == 'POST':
        file = request.files.get('file')
        kwargs = request.form.to_dict()
        user_id = session['id']
        image = UploadImage.main(image=file, uid=user_id)
        if not image:
            return render_template('book/update.html')
        kwargs['state'] = 0
        update_book(bid=bid, image=image, user_id=user_id, **kwargs)
        return redirect(url_for('.upload'))
    page = request.args.get('page')
    return render_template('book/update.html', id=bid, page=page)


@book_bp.route('/finish/')
@book_bp.route('/finish')
@login_required
def finish():
    uid = session['id']
    bid = request.args.get('id')
    state_book(uid=uid, bid=bid, state=3)
    return redirect(url_for('.upload'))


@book_bp.route('/delete/')
@book_bp.route('/delete')
@login_required
def delete():
    uid = session['id']
    bid = request.args.get('id')
    state_book(uid=uid, bid=bid, state=4)
    return redirect(url_for('.upload'))
