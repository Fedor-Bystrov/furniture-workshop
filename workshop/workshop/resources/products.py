import ujson

from workshop.model import Product
from workshop.repository import Repository


class ProductResource:

    def __init__(self, repository: Repository) -> None:
        self._repository = repository
        self._type = Product

    def get_product_list(self) -> str:
        products = self._repository.get_all(self._type)
        product_list = list()
        for product in products:
            product_list.append({
                'productId': product.product_id,
                'name': product.name,
                'creationTime': product.creation_time.isoformat(),
                'categoryId': product.category_id,
                'price': str(product.price),
                'description': product.short_description
            })

        return ujson.dumps(product_list)

    def get_product(self, product_id: int) -> str:
        product = self._repository.get(self._type, product_id)
        if not product:
            # TODO тут кидать более специфичный exception
            raise RuntimeError('Product with id = {} not found!'.format(product_id))

        return ujson.dumps({
            'productId': product.product_id,
            'name': product.name,
            'creationTime': product.creation_time.isoformat(),
            'category': {
                'categoryId': product.category_id,
                'name': product.category.name,
            },
            'price': str(product.price),
            'description': product.description,
        })
