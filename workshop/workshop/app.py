import os

from flask import Flask, Response, abort, request
from sqlalchemy.exc import IntegrityError

from workshop.repository import init_repository
from workshop.resources import categories, products, carts

application_json = 'application/json'

app = Flask(__name__)

_logger = app.logger
_repository = init_repository(
    os.getenv('DB_USR'),
    os.getenv('DB_PASS'),
    os.getenv('DB_HOST'),
    os.getenv('DB_PORT'),
    os.getenv('DB_NAME'),
)

category_resource = categories.CategoryResource(_repository, _logger)
product_resource = products.ProductResource(_repository, _logger)
cart_resource = carts.CartResource(_repository, _logger)


@app.route('/api/category/list', methods=['GET'])
def get_category_list():
    return Response(category_resource.get_category_list(), mimetype=application_json)


@app.route('/api/product/list', methods=['GET'])
def get_product_list():
    return Response(product_resource.get_product_list(), mimetype=application_json)


@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        return Response(product_resource.get_product(product_id), mimetype=application_json)
    except RuntimeError:
        abort(400)


@app.route('/api/cart/list', methods=['GET'])
def get_cart_list():
    return Response(cart_resource.get_cart_list(), mimetype=application_json)


@app.route('/api/cart/<int:cart_id>', methods=['GET'])
def get_cart(cart_id):
    return Response(cart_resource.get_cart(cart_id), mimetype=application_json)


@app.route('/api/cart/<int:cart_id>', methods=['PUT'])
def update_cart(cart_id):
    try:
        request_body = request.get_json(silent=True)
        if not request_body:
            print('empty body')
            raise RuntimeError("Request body is empty!")

        print(request_body)
        cart_resource.update_cart(cart_id, request_body)
        return '', 204

    except (RuntimeError, ValueError):
        abort(400)


@app.route('/api/cart', methods=['POST'])
def create_cart():
    try:
        request_body = request.get_json(silent=True)
        if not request_body:
            print('empty body')
            raise RuntimeError("Request body is empty!")

        print(request_body)
        cart_id = cart_resource.create_cart(request_body)
        return '', 201, {'Location': '/api/cart/{}'.format(cart_id)}

    except (RuntimeError, ValueError, IntegrityError):
        abort(400)


@app.after_request
def after_request(response: Response):
    headers = response.headers
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    headers['Access-Control-Allow-Headers'] = 'Content-Type'
    headers['Access-Control-Expose-Headers'] = 'Location'
    return response
