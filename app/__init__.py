# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.principal import Principal, Permission, RoleNeed
from flask_oauth import OAuth


app = Flask(__name__)
app.config.from_object('app.conf.Config')
db = SQLAlchemy(app)
principals = Principal(app)

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url = 'https://graph.facebook.com/',
    request_token_url = None,
    access_token_url = '/oauth/access_token',
    authorize_url = 'https://www.facebook.com/dialog/oauth',
    consumer_key = app.config['FACEBOOK_CONSUMER_KEY'],
    consumer_secret = app.config['FACEBOOK_CONSUMER_SECRET'],
    request_token_params = {'scope': 'email, manage_pages'}
)


from . import models, views


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(fb_id):
    user = db.session.query(models.User).filter(models.User.fb_id == fb_id)\
        .first()
    if not user:
        return None


@app.before_first_request
def mk_db():
    db.create_all()
