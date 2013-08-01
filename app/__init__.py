# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.principal import Principal, Permission, RoleNeed
from rauth.service import OAuth2Service

app = Flask(__name__)
app.config.from_object('app.conf.Config')


db = SQLAlchemy(app)
principals = Principal(app)


facebook = OAuth2Service (
    name = 'facebook',
    base_url = 'https://graph.facebook.com/',
    access_token_url = 'https://graph.facebook.com/oauth/access_token',
    authorize_url = 'https://www.facebook.com/dialog/oauth',
    client_id = app.config['FACEBOOK_CONSUMER_KEY'],
    client_secret = app.config['FACEBOOK_CONSUMER_SECRET']
)


from . import models, views


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(fb_id):
    return db.session.query(User).filter(User.fb_id == fb_id).first()


@app.before_first_request
def mk_db():
    db.create_all()
