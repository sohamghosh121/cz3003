"""
    FB API
"""

import requests


class TwitterAPI:
    API_KEY = 'J1zlXWbPXeKR7tjgQnM28Moj6'
    API_SECRET = 'XTXYkDtRTZMpKlUD3SkPtudBl6dH4uQWSA1ClqVQFYd07DkQe1'
    ACCESS_TOKEN = '708263718585372672-DoPcGuN849xdwPmIaYjAknYDsAA3iVF'
    ACCESS_SECRET = 'OtnBKub9qERxOLIfqswkAYSPJ7j2R9V3kLhaUzjSkL7dD'
    AUTHORIZE_URL = 'https://api.twitter.com/1.1/statuses/update.json'
    UPDATE_URL = 'http://graph.facebook.com/v2.5/446011332261774/feed'

    def pushUpdate(self, message):
        r = requests.get(self.UPDATE_URL, params={'status': message})
        if r.status_code == 200:
            print(r.text)
        else:
            print(r.status_code)

if __name__ == '__main__':
    fb = FacebookAPI()
    fb.pushUpdate('Test')
