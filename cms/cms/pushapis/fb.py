"""
    FB API
"""

import facebook

class FacebookAPI:
    def pushUpdate(self, message):
        # cfg = {
        #     "page_id": "197027533999861",
        #     "access_token": "CAAYtJqL3ZAO8BAMvOPmWypcZAzAoAEQmWSPMmUfbVY9oJjjOpALsG78bgNYIjpGMvMuW1yOHI9uZCOt328ZCk8QzmrdrkuvhILx5FRBuULK2ecbtBUPVReyZBvcy4WeotcARX7bJmuhhsobb2ZBM5CqhMJkcepkb6w8sOHGWanfZBnetdV2cvX0VcYAZAJc359sZD"
        # }
        # api = self.getAPI(cfg)
        # status = api.put_wall_post(message)
        page_id = "197027533999861"
        page_access_token = "CAAYpV82x7KcBAGA6qrYFL4CDu5akpZBiaO9XRN0Ggx5dmVnKSSiP2ffd4IUCHCc5dA3WtTdbZBUgukHS32jY8YAZC6VSZBuwBqCFDaeGLPa6wvYbNDEiDwXbSoO28RDHpZBFhDXZAZCnZAMUOWl7om2T89zcrAP5kVYsACRXUL9nvHfy3QhToXAuS423OtEiWrX4ZCbYmR3TgNAZDZD"
        graph = facebook.GraphAPI(page_access_token)
        print graph
        graph.put_object(page_id,'feed',message="Hello World!")

    # def getAPI(self, cfg):
    #     graph = facebook.GraphAPI(cfg['access_token'])
    #     # Get page token to post as the page. You can skip 
    #     # the following if you want to post as yourself. 
    #     resp = graph.get_object('me/accounts')
    #     print resp
    #     for page in resp['data']:
    #         if page['id'] == cfg['page_id']:
    #             page_access_token = page['access_token']
    #     graph = facebook.GraphAPI(page_access_token)
    #     print 1
    #     return graph

    # def getAPI(self, message):
    #     page_access_token = "CAAYtJqL3ZAO8BABOAItSxZCedtHmLSUzwMnUzdle5WiOdIaMQZAmHdE2nzaPeT3tlPgUIkuuEZB3m7qqBNB2yD98dgvSLdCas5R4fQzKwazVYqkZAouYqhhQbVI5t2ioBFdmnIRPd29pBdnUg0BYaaspjoma3mB6QYOgvFn5ie8nZCZBL3WzMlm7vrvW8Iq5VKJk1asZCqje1wZDZD"
    #     graph = facebook.GraphAPI(page_access_token)
    #     return graph

# app_access_token = CAAYtJqL3ZAO8BAEx3BRxE2JL3JmUFSduHktpZAL9bjRXD0C6PNvJpw9U2XXVzpBNcWshvSoFRpJg7ZBrYLmkrydcpRKdjAENHQCeZATHt9BWK0q5FC2bKieoNsQgbPa525RO5nByKt0pPvOLCev0nPN95UN3s8gUPUz3mG2c7oyNv5w8qyQODJb8D0DzUc2v7iEqadv7SupuCHJZCQIhvlkAxiV26rZCDtkFd8qOImjwZDZD
# access_token = access_token=CAAYtJqL3ZAO8BAGpvTycn9KCm7CKqXgxpxgk6toCqiZB0hKiOnyFa4YFWnognhPp7eHeuKZA8vckCJnLqo6AaNzdAVezIFQUh1nZBprlVFvOonHXzG3mMexZA9kylZCx6f5mi5uiWU04BHX2MUP5acaSqDynfBdwZCCTHH7aflfbUTpw2uOJM0pmPjkIX8pXxsZD
# # &expires=5184000
# CAAYtJqL3ZAO8BAG893pBwz5jYZBDgA4ZCCv0AlNo5yQiZA9pO3CzNEdk87zA6KSEzDqNUJzyCvxoji3sNSWshLjeYfwslOHZAMADAMfoTMZAMQTEaFrzFj7SQjSnjUDPqWxZCYONXFhC8mYNb5TauqxS8FsrUm3mXOwKwuvuPZA2uAUYobTp2MT5jlszUZCEskGoZD
fb = FacebookAPI()
fb.pushUpdate('Testing')