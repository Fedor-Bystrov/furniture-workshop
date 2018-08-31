import mimetypes
import ujson
import uuid

from falcon import Request, Response, status_codes


class ImagesResource:
    _CHUNK_SIZE_BYTES = 4096
    images = [{'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'}]

    def on_get(self, request: Request, response: Response) -> None:
        response.body = ujson.dumps(self.images, ensure_ascii=False)
        response.status = status_codes.HTTP_200

    def on_post(self, request: Request, response: Response) -> None:
        extension = mimetypes.guess_extension(request.content_type)
        name = b''
        while True:
            chunk = request.stream.read(self._CHUNK_SIZE_BYTES)
            name += chunk
            if not chunk:
                break

        name = name.decode('utf-8').split('.')[0]
        self.images.append({'href:': '/images/{name}_{uuid}{ext}'.format(
            name=name, uuid=uuid.uuid4(), ext=extension)})

        response.status = status_codes.HTTP_201
        response.location = '/images/{}'.format(name)
