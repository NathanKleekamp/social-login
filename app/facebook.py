# -*- coding: utf-8 -*-

import hmac
import json
import hashlib

from base64 import urlsafe_b64decode

import requests

from . import app

app_id = app.config['FACEBOOK_CONSUMER_KEY']
app_secret = app.config['FACEBOOK_CONSUMER_SECRET']


class GraphAPI(object):
    base_url = 'https://graph.facebook.com/{0}/'

    def __init__(self, token):
        self.token = token
        self.installed = []

    def query(self, fb_id='me', **kwargs):
        url = self.base_url.format(fb_id)
        params = {'access_token': self.token}
        params = dict(params.items() + kwargs.items())
        r = requests.get(url, params=params)
        return r

    def app_installs(self, fb_pages):
        '''
        Return a list of dicts with the user's pages that have the TOS
        app installed.

        Return format: [{'id': page}, {'name': page_name}]
        '''
        for page in fb_pages:
            url = 'https://graph.facebook.com/{0}/tabs/{1}?access_token={2}'.\
                  format(page['id'], app_id, self.token)
        r = requests.get(url).json()
        if r['data']:
            self.installed.append(page)
        return self.installed

    @staticmethod
    def me(token):
        graph = GraphAPI(token)
        query = graph.query()
        return query


class SignedRequest(object):

    def __init__(self, signed_request):
        self.signed_request = signed_request
        self.decode_signed_request()

    def __repr__(self):
        pass

    def base64_url_decode(self, arg):
        '''
        Decodes a base64 encoded string. It appends '=' until string is
        divisible by 64.
        '''
        return urlsafe_b64decode(str(arg) + (64 - len(arg) % 64) * "=")

    def decode_signed_request(self):
        '''
        Takes an encoded signed_request, decodes the signature and data,
        check's their legitimacy, and returns the data. See: Canvas Tutorial
        [http://goo.gl/wIbyZ], near the end of the 'Authorization' section.
        '''
        encoded_sig, encoded_data = self.signed_request.split('.', 2)

        self.data = json.loads(self.base64_url_decode(encoded_data))
        self.sig = self.base64_url_decode(encoded_sig)

        if not self.data['algorithm'].upper() == 'HMAC-SHA256':
            raise ValueError('Unknown Algorithm: {0}'.format(self.data['algorithm']))

        expected_sig = hmac.new(app_secret, msg=encoded_data,
                                digestmod=hashlib.sha256).digest()

        if self.sig != expected_sig:
            raise ValueError('Bad Signature')
