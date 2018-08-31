import ujson

from falcon import Request, Response, status_codes


class ImagesResource:

    @staticmethod
    def on_get(request: Request, response: Response) -> None:
        doc = {
            'images': [
                {
                    'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'
                }
            ]
        }

        response.body = ujson.dumps(doc, ensure_ascii=False)
        response.status = status_codes.HTTP_200
