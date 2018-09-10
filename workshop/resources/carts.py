import ujson

from falcon import Request, Response, status_codes, HTTPBadRequest, HTTPInternalServerError
from sqlalchemy.exc import IntegrityError

from workshop.services import cart_service
from workshop.model import Cart
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

            cart_service.update_cart(cart_to_update, ujson.loads(request_body))
            self._repository.save_or_update(cart_to_update)
            response.status = status_codes.HTTP_OK

        except (RuntimeError, ValueError, IntegrityError):
            raise HTTPBadRequest()
        except:
            raise HTTPInternalServerError()


class CreateCartResource:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository
        self._type = Cart

    def on_post(self, request: Request, response: Response) -> None:
        # TODO проверять content-type, если не json, то ошибку
        try:
            request_body = b''
            while True:
                chunk = request.stream.read(_CHUNK_SIZE_BYTES)
                request_body += chunk
                if not chunk:
                    break

            cart = ujson.loads(request_body)
            self._repository.save_or_update(None)  # TODO

        except (RuntimeError, ValueError, IntegrityError):
            raise HTTPBadRequest()
        except:
            raise HTTPInternalServerError()
