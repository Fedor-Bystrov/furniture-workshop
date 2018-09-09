import os

import falcon

from workshop.repository import init_repository
from workshop.resources import products

_repository = init_repository(
    os.getenv('DB_USR'),
    os.getenv('DB_PASS'),
    os.getenv('DB_HOST'),
    os.getenv('DB_PORT'),
    os.getenv('DB_NAME'))

_product_list_resource = products.ProductListResource(_repository)
_product_resource = products.ProductResource(_repository)

api = application = falcon.API()

api.add_route('/api/product/list', _product_list_resource)
api.add_route('/api/product/{product_id:int}', _product_resource)
