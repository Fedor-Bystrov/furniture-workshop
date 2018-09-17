import os

from flask import Flask, Response, abort, request
from sqlalchemy.exc import IntegrityError

from workshop.repository import init_repository
from workshop.resources import categories, products, carts

application_json = 'application/json'

repository = init_repository(
    os.getenv('DB_USR'),
    os.getenv('DB_PASS'),
    os.getenv('DB_HOST'),
    os.getenv('DB_PORT'),
    os.getenv('DB_NAME'),
)

app = Flask(__name__)

category_resource = categories.CategoryResource(repository)
product_resource = products.ProductResource(repository)
cart_resource = carts.CartResource(repository)


@app.route('/api/category/list', methods=['GET'])
def get_category_list():
    return Response(category_resource.get_category_list(), mimetype=application_json)


@app.route('/api/product/list', methods=['GET'])
def get_product_list():
    return Response(product_resource.get_product_list(), mimetype=application_json)


@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return Response(product_resource.get_product(product_id), mimetype=application_json)


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
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Content-Type'
    header['Access-Control-Expose-Headers'] = 'Location'
    return response
