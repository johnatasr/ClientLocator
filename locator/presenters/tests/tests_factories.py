from django.test import TestCase
from locator.presenters.factories import LocatorFactory


class LocatorFactoryTestCase(TestCase):
    """
    Tests of LocatorFactory in locator.presenters.factories.py
    """

    def setUp(self):
        self.factory = LocatorFactory()
        self.data: dict = {
            "pageNumber": 1,
            "pageSize": 10,
            "coordinates": {"lat": -38.9614, "lon": -10.766959},
        }

    def test_search_iterator(self):
        msg = self.factory.create_search_iterator(self.data)
        self.assertIsInstance(msg, dict)

    def test_create_redis_instance(self):
        redis = self.factory.create_redis_instance()
        self.assertIsInstance(redis, object)

    def test_create_base_by_json(self):
        redis = self.factory.create_redis_instance()
        result = self.factory.create_base_by_json(redis_instance=redis)
        self.assertIsInstance(result, str)
        self.assertEquals(result, "Base import successful")

    def test_create_base_by_csv(self):
        redis = self.factory.create_redis_instance()
        result = self.factory.create_base_by_csv(redis_instance=redis)
        self.assertIsInstance(result, str)
        self.assertEquals(result, "Base import successful")
