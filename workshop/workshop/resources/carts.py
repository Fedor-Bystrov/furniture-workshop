import ujson

from workshop.model import Cart
from workshop.repository import Repository
from workshop.services import cart_service


class CartResource:

    def __init__(self, repository: Repository) -> None:
        self._repository = repository
        self._type = Cart

    def get_cart_list(self) -> str:
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

        return ujson.dumps(cart_list)

    def get_cart(self, cart_id: int) -> str:
        cart = self._repository.get(self._type, cart_id)
        if not cart:
            raise RuntimeError('Cart with id = {} not found!'.format(cart_id))

        return ujson.dumps({
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

    def update_cart(self, cart_id: int, request_data: dict) -> None:
        cart_to_update = self._repository.get(self._type, cart_id)
        if not cart_to_update:
            raise RuntimeError('Cart with id = {} not found!'.format(cart_id))

        cart_service.update_cart(cart_to_update, request_data)
        self._repository.save_or_update(cart_to_update)

    def create_cart(self, request_data: dict) -> None:
        self.validate(request_data)

        cart = cart_service.create_cart(request_data)
        self._repository.save_or_update(cart)
        return ujson.dumps({'cartId': cart.cart_id})

    @staticmethod
    def validate(request_body: dict):
        required_fields = [
            'firstName', 'lastName', 'middleName', 'email', 'phone',
            'shippingAddress', 'purchases', 'price', 'description'
        ]

        keys = request_body.keys()
        for field in required_fields:
            if field not in keys:
                raise RuntimeError('field "{}" is required'.format(field))
