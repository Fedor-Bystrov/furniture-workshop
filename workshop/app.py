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

_product_resource = products.ProductResource(_repository)

api = application = falcon.API()
api.add_route('/images', images.ImagesResource())

api.add_route('/product/list', _product_resource)
api.add_route('/product/{product_id:int}', _product_resource)
