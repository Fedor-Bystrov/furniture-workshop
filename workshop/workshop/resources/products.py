import ujson
from logging import Logger

from workshop.model import Product
from workshop.repository import Repository


class ProductResource:

    def __init__(self, repository: Repository, logger: Logger) -> None:
        self._repository = repository
        self.logger = logger
        self._type = Product

    def get_product_list(self) -> str:
        products = self._repository.get_all(self._type)
        if not products:
            self.logger.debug("[products.get_product_list]: error, cannot fetch products from database")
            raise RuntimeError("Error, database returned zero products")

        product_list = list()
        for product in products:
            product_list.append({
                'productId': product.product_id,
                'name': product.name,
                'categoryId': product.category_id,
                'description': product.short_description
            })

        return ujson.dumps(product_list)

    def get_product(self, product_id: int) -> str:
        product = self._repository.get(self._type, product_id)
        if not product:
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
