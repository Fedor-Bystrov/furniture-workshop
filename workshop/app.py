import falcon

from .resources.images import ImagesResource

api = application = falcon.API()
api.add_route('/images', ImagesResource())
