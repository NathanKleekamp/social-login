# -*- coding: utf-8 -*-

from . import db

class User(db.Model):
    '''Page user'''
    id = db.Column(db.Integer, primary_key=True)
    fb_id = db.Column(db.BigInteger, nullable=False, unique=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    admin = db.Column(db.Boolean)


    def __init__(self, fb_id, name, email):
        self.fb_id = fb_id
        self.name = name
        self.email = email

    def __repr__(self):
        return '< User: {0} >'.format(self.name)

    @staticmethod
    def get_or_create(fb_id, username, email):
        user = db.session.query(User).filter(User.fb_id == fb_id).first()
        if not user:
            user = User(fb_id, username, email)
            db.session.add(user)
            db.session.commit()
        return user