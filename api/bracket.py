import falcon
from pymongo import MongoClient
import json


class Brackets(object):

    def on_get(self, req, resp):
        client = MongoClient()
        collection = client.lol.brackets
        query = {}
        resp.body = json.dumps(list(collection.find(query)))
        resp.status = falcon.HTTP_200
