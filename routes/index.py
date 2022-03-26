from flask import Blueprint, render_template

from models.book import index_book

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
    book = index_book()
    return render_template('index.html', book=book)
