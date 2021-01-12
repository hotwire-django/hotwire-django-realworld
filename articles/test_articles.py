from django.test import TestCase
from django.test import Client


class MyTest(TestCase):
    fixtures = ["data.yaml"]

    def test_list(self):
        response = Client().get("/article/")
        assert response.status_code == 200
        assert b"How to build webapps that scale" in response.content
