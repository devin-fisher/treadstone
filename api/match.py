import falcon
from pymongo import MongoClient
import json


class Matches(object):

    def on_get(self, req, resp, bracket_id):
        print(bracket_id)
        client = MongoClient()
        collection = client.lol.scheduled_games
        query = {'bracket_id':bracket_id}
        print(query)
        resp.body = json.dumps(list(collection.find(query)))
        resp.status = falcon.HTTP_200
