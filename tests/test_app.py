import falcon
import pytest
import ujson
from falcon import testing

from workshop.app import api


@pytest.fixture
def client():
    return testing.TestClient(api)


# TODO pytest тут не нужен
def test_list_images(client):
    doc = {
        'images': [
            {
                'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'
            }
        ]
    }

    response = client.simulate_get('/images')
    result_doc = ujson.decode(response.content)

    assert result_doc == doc
    assert response.status == falcon.HTTP_OK
