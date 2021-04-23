from locator.presenters.validators import LocatorValidator
from django.test import TestCase
import unittest


class LocatorValidatorTestCase(TestCase):
    """
    Tests of LocatorValidator in locator.presenters.validators.py
    """

    def setUp(self):
        self.validator = LocatorValidator()
        self.data: dict = {
            "pageNumber": 1,
            "pageSize": 10,
            "coordinates": {"lat": -38.9614, "lon": -10.766959},
        }

    def test_validate(self):
        self.assertEquals(self.validator.validate(True), True)
        self.assertEquals(self.validator.validate(False), False)

    def test_is_empty_payload(self):
        result = self.validator.is_empty_payload(self.data)
        self.assertEquals(result, True)

    @unittest.expectedFailure
    def test_is_empty_payload_fail(self):
        self.validator.is_empty_payload(None)

    def test_validate_only_coordinates(self):
        coords: dict = {"lat": -38.9614, "lon": -10.766959}
        result = self.validator.validate_coordinates(coords)
        self.assertEquals(result, True)

    @unittest.expectedFailure
    def test_validate_only_coordinates_fail(self):
        coords: dict = {"coordinates": {"lon": -10.766959}}
        self.validator.validate_coordinates(coords)

    def test_validate_payload(self):
        result = self.validator.validate_payload(self.data)
        self.assertEquals(result, True)

    @unittest.expectedFailure
    def test_validate_payload(self):
        self.validator.validate_payload(None)
