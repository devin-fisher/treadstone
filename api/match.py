import falcon
from pymongo import MongoClient
import json


class Matches(object):

    def on_get(self, req, resp, bracket_id):
        client = MongoClient()
        collection = client.lol.scheduled_matches
        query = {'bracket_id':bracket_id}
        resp.body = json.dumps(list(collection.find(query)))
        resp.status = falcon.HTTP_200

class Game(object):
    def on_get(self, req, resp, bracket_id, match_id, game_id):
        print('hi')
        client = MongoClient()
        collection = client.lol.scheduled_matches
        pipeline = [
          {'$match': {'id' : match_id}},
          {'$unwind' : '$games' },
          {'$match': {'games.gameId' : game_id}},
          {'$project': {'_id': 0, 'games': 1}}
        ]
        print(pipeline)
        game = collection.aggregate(pipeline)['result']
        game = game[0] if len(game) >= 1 else None
        print(game)
        if game and 'games' in game:
            resp.body = json.dumps(game['games'])
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404
