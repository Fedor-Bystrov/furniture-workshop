import os

import falcon

from workshop.repository import init_repository
from workshop.resources import categories, carts, products

_repository = init_repository(
    os.getenv('DB_USR'),
    os.getenv('DB_PASS'),
    os.getenv('DB_HOST'),
    os.getenv('DB_PORT'),
    os.getenv('DB_NAME'))

_category_list_resource = categories.CategoryListResource(_repository)
_product_list_resource = products.ProductListResource(_repository)
_product_resource = products.ProductResource(_repository)
_cart_list_resource = carts.CartListResource(_repository)


api = application = falcon.API()

api.add_route('/api/category/list', _category_list_resource)
api.add_route('/api/product/list', _product_list_resource)
api.add_route('/api/product/{product_id:int}', _product_resource)
api.add_route('/api/cart/list', _cart_list_resource)
# api.add_route('/api/cart/{product_id:int}', _product_resource)

