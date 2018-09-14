import ujson

from workshop.model import Category
from workshop.repository import Repository


class CategoryResource:

    def __init__(self, repository: Repository) -> None:
        self._repository = repository
        self._type = Category

    def get_category_list(self) -> str:
        categories = self._repository.get_all(self._type)
        category_list = list()
        for category in categories:
            category_list.append({
                'categoryId': category.category_id,
                'name': category.name,
            })

        return ujson.dumps(category_list)
