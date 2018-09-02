import ujson

from falcon import Request, Response, status_codes, HTTPBadRequest

from workshop.model import Product
from workshop.repository import Repository


class ProductListResource:

    def __init__(self, repository: Repository) -> None:
        self._repository = repository
        self._type = Product

    def on_get(self, request: Request, response: Response) -> None:
        products = self._repository.get_all(self._type)
        product_list = list()
        for product in products:
            product_list.append({
                'id': product.id,
                'name': product.name,
                'creationTime': product.creation_time.isoformat(),
                'categoryId': product.category_id,
                'price': str(product.price),
            })

        response.body = ujson.dumps(product_list)
        response.status = status_codes.HTTP_OK


class ProductResource:
    _CHUNK_SIZE_BYTES = 4096

    def __init__(self, repository: Repository) -> None:
        self._repository = repository
        self._type = Product

    def on_get(self, request: Request, response: Response, product_id: int) -> None:
        try:
            product = self._repository.get(self._type, product_id)
            if not product:
                # TODO тут кидать более специфичный exception
                raise RuntimeError('Product with id = {} not found!'.format(product_id))

            response.body = ujson.dumps({
                'id': product.id,
                'name': product.name,
                'creationTime': product.creation_time.isoformat(),
                'categoryId': product.category_id,
                'price': str(product.price),
            })
            response.status = status_codes.HTTP_OK

        except RuntimeError:
            raise HTTPBadRequest()
