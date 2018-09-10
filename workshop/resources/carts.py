import ujson
from datetime import datetime
from decimal import Decimal

from falcon import Request, Response, status_codes, HTTPBadRequest

from workshop.model import Cart, Purchase
from workshop.repository import Repository

_CHUNK_SIZE_BYTES = 4096


class CartListResource:

    def __init__(self, repository: Repository) -> None:
        self._repository = repository
        self._type = Cart

    def on_get(self, request: Request, response: Response) -> None:
        carts = self._repository.get_all(self._type)
        cart_list = list()
        for cart in carts:
            cart_list.append({
                'cartId': cart.cart_id,
                'creationTime': cart.creation_time.isoformat(),
                'customerId': cart.customer_id,
                'price': str(cart.price),
                'description': cart.description,
                'shippingAddress': cart.shipping_address,
            })

        response.body = ujson.dumps(cart_list)
        response.status = status_codes.HTTP_OK


class GetUpdateCartResource:

    def __init__(self, repository: Repository) -> None:
        self._repository = repository
        self._type = Cart

    def on_get(self, request: Request, response: Response, cart_id: int) -> None:
        try:
            cart = self._repository.get(self._type, cart_id)
            if not cart:
                # TODO тут кидать более специфичный exception
                raise RuntimeError('Cart with id = {} not found!'.format(cart_id))

            response.body = ujson.dumps({
                'cartId': cart.cart_id,
                'creationTime': cart.creation_time.isoformat(),
                'customer': {
                    'customerId': cart.customer_id,
                    'creationTime': cart.customer.creation_time.isoformat(),
                    'firstName': cart.customer.first_name,
                    'lastName': cart.customer.last_name,
                    'middleName': cart.customer.middle_name,
                    'locale': cart.customer.locale.value,
                    'email': cart.customer.email,
                    'phone': cart.customer.phone,
                },
                'price': str(cart.price),
                'purchases': [{'productId': p.product_id, 'quantity': p.quantity} for p in cart.purchases],
                'description': cart.description,
                'shippingAddress': cart.shipping_address,
            })
            response.status = status_codes.HTTP_OK

        except RuntimeError:
            raise HTTPBadRequest()

    def on_put(self, request: Request, response: Response, cart_id: int) -> None:
        # TODO проверять content-type, если не json, то ошибку
        try:
            cart_to_update = self._repository.get(self._type, cart_id)
            if not cart_to_update:
                # TODO тут кидать более специфичный exception
                raise RuntimeError('Cart with id = {} not found!'.format(cart_id))

            request_body = b''
            while True:
                chunk = request.stream.read(_CHUNK_SIZE_BYTES)
                request_body += chunk
                if not chunk:
                    break

            self.update_cart(cart_to_update, ujson.loads(request_body))
            print('save_or_update')
            self._repository.save_or_update(cart_to_update)
            response.status = status_codes.HTTP_OK
            print('return!')

        except (RuntimeError, ValueError):
            raise HTTPBadRequest()

    def update_cart(self, cart_to_update: Cart, request_body):
        first_name = request_body.get('firstName')
        if first_name:
            cart_to_update.customer.first_name = first_name

        last_name = request_body.get('lastName')
        if last_name:
            cart_to_update.customer.last_name = last_name

        middle_name = request_body.get('middleName')
        if middle_name:
            cart_to_update.customer.middle_name = middle_name

        email = request_body.get('email')
        if email:
            cart_to_update.customer.email = email

        phone = request_body.get('phone')
        if phone:
            cart_to_update.customer.phone = phone

        shipping_address = request_body.get('shippingAddress')
        if shipping_address:
            cart_to_update.shipping_address = shipping_address

        purchases = request_body.get('purchases')
        if purchases:
            for purchase in purchases:
                product_id = purchase.get('productId')
                quantity = purchase.get('quantity')
                if product_id and quantity:
                    self.update_purchase(cart_to_update, product_id, quantity)

        price = request_body.get('price')
        if price:
            cart_to_update.price = Decimal(price)

        description = request_body.get('description')
        if description:
            cart_to_update.description = description

    @staticmethod
    def update_purchase(cart_to_update, product_id, quantity):
        purchase_to_update = list(filter(lambda p, p_id=product_id: p.product_id == p_id,
                                         cart_to_update.purchases))
        if len(purchase_to_update) > 0:
            purchase_to_update[0].quantity = quantity
        else:
            cart_to_update.purchases.append(Purchase(creation_time=datetime.now(),
                                                     cart_id=cart_to_update.cart_id,
                                                     product_id=product_id,
                                                     quantity=quantity))


class CreateCartResource:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository
        self._type = Cart

    def on_post(self, request: Request, response: Response) -> None:
        pass
    # TODO
