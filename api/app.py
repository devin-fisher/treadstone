import falcon
import match
import bracket
 
# falcon.API instances are callable WSGI apps
wsgi_app = api = falcon.API()
 
# Resources are represented by long-lived class instances
brackets = bracket.Brackets()
matches = match.Matches()

 
# things will handle all requests to the '/things' URL path
api.add_route('/api/brackets', brackets)
api.add_route('/api/brackets/{bracket_id}/matches', matches)
