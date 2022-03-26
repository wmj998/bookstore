from flask import Blueprint, render_template, request, redirect, url_for, session

from models.book import query_id
from models.cart import add_cart, query_cart, query_uid, delete_cart, update_cart, add_number
from tools.user import login_required

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


@cart_bp.route('')
@login_required
def index():
    uid = session['id']
    res = query_uid(uid=uid)
    number = sum([i.number for i in res])
    subtotal = sum([i.number * i.book.price for i in res])
    return render_template('cart/index.html', res=res, number=number, subtotal=subtotal)


@cart_bp.route('/add/')
@cart_bp.route('/add')
@login_required
def add():
    bid = request.args.get('id')
    uid = session['id']
    cart = query_cart(uid=uid, bid=bid)
    if cart:
        add_number(cid=cart.id)
    else:
        add_cart(uid=uid, bid=bid)
    return redirect(url_for('.index'))


@cart_bp.route('/detail/')
@cart_bp.route('/detail')
@login_required
def detail():
    bid = request.args.get('id')
    book = query_id(bid=bid)
    return render_template('cart/detail.html', book=book)


@cart_bp.route('/delete/')
@cart_bp.route('/delete')
@login_required
def delete():
    cid = request.args.get('id')
    delete_cart(cid=cid)
    return redirect(url_for('.index'))


@cart_bp.route('/update/', methods=['GET', 'POST'])
@cart_bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    cid = request.args.get('id')
    if request.method == 'POST':
        number = request.form.get('quantity')
        update_cart(cid=cid, number=number)
        return redirect(url_for('.index'))
    return render_template('cart/update.html', id=cid)
