from locator.domain.entities import list_users as lu, classification as cl
from django.test import TestCase
import pandas as pd


class ClassificationEntityTestCase(TestCase):
    """
    Tests of Classification in locator.domain.entities.classification.py
    """

    def setUp(self):
        self.classification1 = cl.Classification(lat=-38.9614, lon=-10.766959)
        self.classification2 = cl.Classification(lat=-68.9614, lon=70.766959)

    def test_isistance_object(self):
        self.assertIsInstance(self.classification1, cl.Classification)
        self.assertIsInstance(self.classification1, cl.Classification)

    def test_atributes_values(self):
        self.assertEquals(self.classification1.lat, -38.9614)
        self.assertEquals(self.classification1.lon, -10.766959)
        self.classification1.get_classification()
        self.assertEquals(self.classification1.minlat[0], -46.361899)
        self.assertEquals(self.classification1.maxlat[0], -34.276938)
        self.assertEquals(self.classification1.minlon[0], -2.196998)
        self.assertEquals(self.classification1.maxlon[0], -15.411580)
        self.assertEquals(self.classification1.name, "ESPECIAL1")

        self.assertEquals(self.classification2.lat, -68.9614)
        self.assertEquals(self.classification2.lon, 70.766959)
        self.classification2.get_classification()
        self.assertEquals(self.classification2.minlat[0], -98.9614)
        self.assertEquals(self.classification2.maxlat[0], -38.9614)
        self.assertEquals(self.classification2.minlon[0], 40.766959)
        self.assertEquals(self.classification2.maxlon[0], 100.766959)
        self.assertEquals(self.classification2.name, "TRABALHOSO")

    def test_atributes_type(self):
        self.assertIsInstance(self.classification1.lat, float)
        self.assertIsInstance(self.classification1.lon, float)
        self.classification1.get_classification()
        self.assertIsInstance(self.classification1.minlat[0], float)
        self.assertIsInstance(self.classification1.maxlat[0], float)
        self.assertIsInstance(self.classification1.minlon[0], float)
        self.assertIsInstance(self.classification1.maxlon[0], float)
        self.assertIsInstance(self.classification1.name, str)

        self.assertIsInstance(self.classification2.lat, float)
        self.assertIsInstance(self.classification2.lon, float)
        self.classification2.get_classification()
        self.assertIsInstance(self.classification2.minlat[0], float)
        self.assertIsInstance(self.classification2.maxlat[0], float)
        self.assertIsInstance(self.classification2.minlon[0], float)
        self.assertIsInstance(self.classification2.maxlon[0], float)
        self.assertIsInstance(self.classification2.name, str)

    def test_repr_class(self):

        repr1: str = "Entity: Classification<lat: -38.9614, lon: -10.766959>"
        repr2: str = "Entity: Classification<lat: -68.9614, lon: 70.766959>"

        self.assertEquals(self.classification1.__str__(), repr1)
        self.assertEquals(self.classification2.__str__(), repr2)


class ListUsersEntityTestCase(TestCase):
    """
    Tests of ListUsersin locator.domain.entities.list_users.py
    """

    def setUp(self):
        self.classification1 = cl.Classification(lat=-38.9614, lon=-10.766959)
        self.classification1.get_classification()
        self.classification2 = cl.Classification(lat=-68.9614, lon=70.766959)
        self.classification2.get_classification()

        self.list_user1 = lu.ListUsers(
            users=pd.DataFrame([[1, 1.23, "Hello"]], columns=list("ABC")),
            classification=self.classification1,
        )
        self.list_user2 = lu.ListUsers(
            users=pd.DataFrame([[1, 1.23, "Hello"]], columns=list("ABC")),
            classification=self.classification2,
        )

    def test_isistance_object(self):
        self.assertIsInstance(self.list_user1, lu.ListUsers)
        self.assertIsInstance(self.list_user2, lu.ListUsers)

    def test_atributes_values(self):
        self.assertEquals(self.list_user1.users.iloc[0]["A"], 1)
        self.assertEquals(self.list_user1.classification.name, "ESPECIAL1")

        self.assertEquals(self.list_user2.users.iloc[0]["C"], "Hello")
        self.assertEquals(self.list_user2.classification.name, "TRABALHOSO")

    def test_atributes_type(self):
        self.assertIsInstance(self.list_user1.users, pd.DataFrame)
        self.assertIsInstance(self.list_user1.classification, cl.Classification)

        self.assertIsInstance(self.list_user2.users, pd.DataFrame)
        self.assertIsInstance(self.list_user2.classification, cl.Classification)

    def test_repr_class(self):
        repr: str = "Entity: ListUsers<>"

        self.assertEquals(self.list_user1.__str__(), repr)
        self.assertEquals(self.list_user2.__str__(), repr)
