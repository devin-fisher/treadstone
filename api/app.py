import falcon
import match
 
class ThingsResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.body = 'Hello world!'
 
# falcon.API instances are callable WSGI apps
wsgi_app = api = falcon.API()
 
# Resources are represented by long-lived class instances
things = ThingsResource()
matches = match.Matches()
 
# things will handle all requests to the '/things' URL path
api.add_route('/api', things)
api.add_route('/api/{bracket_id}/matches', matches)