# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, session
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from flask.ext.principal import Permission, RoleNeed

from . import app, db, facebook, login_manager
from .models import User
from .facebook import GraphAPI

admin_permission = Permission(RoleNeed('admin'))


@app.route('/')
def index():
    print(current_user.is_authenticated())
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(response):
    if response is None:
        # In a real case, this should return error message/description
        return redirect(url_for('test'))

    token = response['access_token']

    me = GraphAPI.me(token).json()

    user = User.get_or_create(me['id'], me['name'], me['email'])

    login_user(user)

    print (current_user.is_authenticated())

    return redirect(url_for('index'))


@facebook.tokengetter
def get_facebook_oauth_token():
    if current_user.is_authenticated():
        return (current_user.token, current_user.secret)
    else:
        return None


@login_manager.user_loader
def load_user(fb_id):
    user = db.session.query(User).filter(User.fb_id == fb_id)\
        .first()
    if not user:
        return None
    else:
        return user


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/test')
@login_required
def test():
    return render_template('test.html')
