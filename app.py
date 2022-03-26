import os
from datetime import timedelta

from flask import Flask
from flask_wtf import CSRFProtect

app = Flask(__name__)

app.config.from_json('conf.json')

# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

uri = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}'.format(**app.config['MYSQL'])
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CSRFProtect(app)
