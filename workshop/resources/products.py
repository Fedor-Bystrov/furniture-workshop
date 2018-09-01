import ujson

from falcon import Request, Response, status_codes

from workshop.model import Product
from workshop.repository import Repository


class ProductResource:

    def __init__(self, repository: Repository) -> None:
        super().__init__()
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
        response.status = status_codes.HTTP_200

