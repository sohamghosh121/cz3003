"""
    FB API
"""

import tweepy


class FacebookAPI:
    UPDATE_URL = 'http://graph.facebook.com/v2.5/446011332261774/feed'

    def pushUpdate(self, message):
        r = requests.get(self.UPDATE_URL, params={'message': message})
        if r.status_code == 200:
            print(r.text)
        else:
            print(r.status_code)

if __name__ == '__main__':
    fb = FacebookAPI()
    fb.pushUpdate('Test')
