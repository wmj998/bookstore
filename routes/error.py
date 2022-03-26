from flask import render_template


def error_404(e):
    return render_template('error/404.html')
