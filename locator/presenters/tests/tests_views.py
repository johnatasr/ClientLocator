from rest_framework import status
from rest_framework.test import APITestCase
import unittest


class LocatorViewSetTests(APITestCase):
    """
    Tests of LocatorViewSet in locator.presenters.views.py
    """

    def setUp(self):
        self.data: dict = {
            "pageNumber": 1,
            "pageSize": 10,
            "coordinates": {"lat": -38.9614, "lon": -10.766959},
        }

    def test_search_with_data(self):
        response = self.client.post("/search", data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_no_page_number(self):
        wrong_data: dict = {
            "pageSize": 10,
            "coordinates": {"lat": -38.9614, "lon": -10.766959},
        }
        response = self.client.post("/search", data=wrong_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            response.json.args[0].data["msg"], "Field required: pageNumber"
        )

    def test_search_no_page_size(self):
        wrong_data: dict = {
            "pageNumber": 1,
            "coordinates": {"lat": -38.9614, "lon": -10.766959},
        }
        response = self.client.post("/search", data=wrong_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json.args[0].data["msg"], "Field required: pageSize")

    def test_search_no_coordinates(self):
        wrong_data: dict = {"pageSize": 10, "pageNumber": 1}
        response = self.client.post("/search", data=wrong_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            response.json.args[0].data["msg"], "Field required: coordinates"
        )

    def test_search_wrong_data(self):
        wrong_data: dict = {
            "pageNumber": 1,
            "pageSize": 10,
        }
        response = self.client.post("/search", data=wrong_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_no_data(self):
        response = self.client.post("/search")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
