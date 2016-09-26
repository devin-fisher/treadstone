import falcon
from wsgiref import simple_server
from league import *
from report import *
 
# falcon.API instances are callable WSGI apps
wsgi_app = api = application = falcon.API()
 
# Resources are represented by long-lived class instances
league = League()
league_list = LeagueList()
tournament = Tournament()
tournament_list = TournamentList()
bracket = Bracket()
bracket_list = BracketList()
report = Report()
match = Match()
match_list = MatchList()
game = Game()
game_list = GameList()


api.add_route("/api/leagues/", league_list)
api.add_route("/api/leagues/{league_id}/", league)
api.add_route("/api/leagues/{league_id}/tournaments/", tournament_list)
api.add_route("/api/leagues/{league_id}/tournaments/{tournament_id}", tournament)
api.add_route("/api/leagues/{league_id}/tournaments/{tournament_id}/brackets/", bracket_list)
api.add_route("/api/leagues/{league_id}/tournaments/{tournament_id}/brackets/{bracket_id}", bracket)
api.add_route("/api/leagues/{league_id}/tournaments/{tournament_id}/brackets/{bracket_id}/matches/", match_list)
api.add_route("/api/leagues/{league_id}/tournaments/{tournament_id}/brackets/{bracket_id}/matches/{match_id}", match)
api.add_route("/api/leagues/{league_id}/tournaments/{tournament_id}/brackets/{bracket_id}/matches/{match_id}/report", report)
api.add_route("/api/leagues/{league_id}/tournaments/{tournament_id}/brackets/{bracket_id}/matches/{match_id}/games/", game_list)
api.add_route("/api/leagues/{league_id}/tournaments/{tournament_id}/brackets/{bracket_id}/matches/{match_id}/games/{game_id}", game)

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8555, application)
    httpd.serve_forever()
