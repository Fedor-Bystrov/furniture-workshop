import ujson
from unittest import TestCase

import falcon
from falcon import testing

from workshop.app import api


class AppTest(TestCase):

    @staticmethod
    def client_fixture():
        return testing.TestClient(api)

    def test_list_images(self):
        doc = {'images': [{'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'}]}

        response = self.client_fixture().simulate_get('/images')
        result_doc = ujson.decode(response.content)

        self.assertEqual(doc, result_doc)
        self.assertEqual(response.status, falcon.HTTP_OK)
