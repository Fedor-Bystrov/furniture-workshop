import ujson
from logging import Logger

from workshop.model import Category
from workshop.repository import Repository


class CategoryResource:

    def __init__(self, repository: Repository, logger: Logger) -> None:
        self.repository = repository
        self.logger = logger
        self.type = Category

    def get_category_list(self) -> str:
        categories = self.repository.get_all(self.type)
        if not categories:
            self.logger.debug("[categories.get_category_list]: error, cannot fetch categories from database")
            raise RuntimeError("Error, database returned zero categories")

        category_list = list()
        for category in categories:
            category_list.append({
                'categoryId': category.category_id,
                'name': category.name,
            })

        return ujson.dumps(category_list)
