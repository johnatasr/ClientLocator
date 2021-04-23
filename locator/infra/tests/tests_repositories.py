from locator.infra.repositories import LocatorRepo
from locator.domain.entities import list_users as lu, classification as clo
from locator.presenters.factories import LocatorFactory
from django.test import TestCase
import pandas as pd


class LocatorRepoTestCase(TestCase):
    """
    Tests of LocatorRepo in locator.infra.repositories.py
    """

    def setUp(self):
        redis = LocatorFactory().create_redis_instance()
        self.repo = LocatorRepo(redis_instance=redis)

    def test_clients_by_position(self):
        list_users = self.repo.get_clients_by_position(lat=-38.9614, lon=-10.766959)
        self.assertIsInstance(list_users, lu.ListUsers)
        self.assertEquals(len(list_users.users), 4)
        list_users.classification.get_classification()
        self.assertEquals(list_users.classification.name, "ESPECIAL1")

    def test_get_all_data(self):
        df = self.repo.get_all_data()
        self.assertIsInstance(df, pd.DataFrame)

    def test_create_classification(self):
        clas_entity = self.repo.create_classification(lat=-38.9614, lon=-10.766959)
        self.assertIsInstance(clas_entity, clo.Classification)
        self.assertEquals(clas_entity.get_classification(), "ESPECIAL1")

    def test_create_list_users(self):
        clas_entity = self.repo.create_classification(lat=-38.9614, lon=-10.766959)
        users = self.repo.get_all_data()
        list_users = self.repo.create_list_users(
            classification=clas_entity, users=users
        )
        self.assertIsInstance(list_users, lu.ListUsers)
        list_users.classification.get_classification()
        self.assertEquals(list_users.classification.name, "ESPECIAL1")
        self.assertEquals(len(list_users.users), 2000)
