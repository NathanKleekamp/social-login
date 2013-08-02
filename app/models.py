# -*- coding: utf-8 -*-

from . import db

class User(db.Model):
    '''Page user'''
    id = db.Column(db.Integer, primary_key=True)
    fb_id = db.Column(db.BigInteger, nullable=False, unique=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    admin = db.Column(db.Boolean)
    active = db.Column(db.Boolean, nullable=False, default=True)


    def __init__(self, fb_id, name, email):
        self.fb_id = fb_id
        self.name = name
        self.email = email

    def __repr__(self):
        return '< User: {0} >'.format(self.name)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.fb_id)

    @staticmethod
    def get_or_create(fb_id, name, email):
        user = User.query.filter_by(fb_id=fb_id).first()
        if user is None:
            user = User(fb_id, name, email)
            db.session.add(user)
            db.session.commit()
        return user
