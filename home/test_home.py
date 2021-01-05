from django.test import TestCase
from django.test import Client


class MyTest(TestCase):
    fixtures = ["data.yaml"]

    def test_index(self):
        response = Client().get("/")
        assert response.status_code == 200
        assert b"conduit" in response.content
        assert b"How to build webapps that scale" in response.content
        assert b"emberjs" in response.content
