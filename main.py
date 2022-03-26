from app import app
from routes.book import book_bp
from routes.cart import cart_bp
from routes.error import error_404
from routes.index import index_bp
from routes.manager import manager_bp
from routes.user import user_bp

app.register_blueprint(book_bp)
app.register_blueprint(cart_bp)
app.register_error_handler(404, error_404)
app.register_blueprint(index_bp)
app.register_blueprint(manager_bp)
app.register_blueprint(user_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
