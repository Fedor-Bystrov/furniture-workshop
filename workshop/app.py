import os

import falcon

from workshop.repository import init_repository
from workshop.resources import images, products

_repository = init_repository(
    os.getenv('DB_USR'),
    os.getenv('DB_PASS'),
    os.getenv('DB_HOST'),
    os.getenv('DB_PORT'),
    os.getenv('DB_NAME'))

api = application = falcon.API()
api.add_route('/images', images.ImagesResource())
api.add_route('/product', products.ProductResource(_repository))
