# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for

from . import app, facebook
from .models import User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    redirect_uri = url_for('authorized', _external=True)
    params = {'redirect_uri': redirect_uri,
              'scope': 'email,manage_pages'}
    return redirect(facebook.get_authorize_url(**params))


@app.route('/authorized')
def authorized():
    if not 'code' in request.args:
        return 'You declined'

    redirect_uri = url_for('authorized', _external=True)
    data = dict(code=request.args['code'], redirect_uri=redirect_uri)

    session = facebook.get_auth_session(data=data)

    me = session.get('me').json()

    User.get_or_create(me['id'], me['username'], me['email'])

    return redirect(url_for('index'))


@app.route('/test')
def test():
    return render_template('test.html')
