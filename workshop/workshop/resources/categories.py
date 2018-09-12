import ujson

from falcon import Request, Response, status_codes

from workshop.model import Category
from workshop.repository import Repository


class CategoryListResource:

    def __init__(self, repository: Repository) -> None:
        self._repository = repository
        self._type = Category

    def on_get(self, request: Request, response: Response) -> None:
        categories = self._repository.get_all(self._type)
        category_list = list()
        for category in categories:
            category_list.append({
                'categoryId': category.category_id,
                'name': category.name,
            })

        response.body = ujson.dumps(category_list)
        response.status = status_codes.HTTP_OK
