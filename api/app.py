import falcon
from wsgiref import simple_server
from league import Tournament, League, Bracket, Match, Game
 
# falcon.API instances are callable WSGI apps
wsgi_app = api = application = falcon.API()
 
# Resources are represented by long-lived class instances
league = League()
tournament = Tournament()
bracket = Bracket()
match = Match()
game = Game()


api.add_route("/api/league/{league_id}/", league)
api.add_route("/api/league/{league_id}/tournaments/{tournament_id}", tournament)
api.add_route("/api/league/{league_id}/tournaments/{tournament_id}/brackets/{bracket_id}", bracket)
api.add_route("/api/league/{league_id}/tournaments/{tournament_id}/brackets/{bracket_id}/matches/{match_id}", match)
api.add_route("/api/league/{league_id}/tournaments/{tournament_id}/brackets/{bracket_id}/matches/{match_id}/games/{game_id}", game)

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, application)
    httpd.serve_forever()
