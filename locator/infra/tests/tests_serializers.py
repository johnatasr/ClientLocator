from locator.presenters.iterators import DataLoadIterator
from locator.presenters.factories import LocatorFactory
from locator.presenters.helpers import LocatorHelpers
from locator.infra.serializers import DefaultSerializer
from locator.domain.entities import list_users as lu, classification as cl
from django.test import TestCase


class DefaultSerializerTestCase(TestCase):
    """
    Tests of DefaultSerializer in locator.infra.serializer.py
    """

    def setUp(self):
        INPUT_CSV: str = "https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv"

        self.helpers = LocatorHelpers()
        self.iterator = DataLoadIterator(
            redis=LocatorFactory().create_redis_instance(), helper=LocatorHelpers()
        )
        self.df = self.helpers.format_dataframe(
            df=self.iterator._create_dataframe_from_csv(INPUT_CSV)
        )
        self.classification = cl.Classification(lat=-38.9614, lon=-10.766959)
        self.classification.get_classification()
        self.list_users = lu.ListUsers(
            users=self.df, classification=self.classification
        )

        self.serializer = DefaultSerializer

    def test_init(self):
        serializer = self.serializer(
            list_users=self.list_users, page_number=1, page_size=12
        )
        self.assertIsInstance(serializer.list_users, lu.ListUsers)
        self.assertIsInstance(serializer.page_number, int)
        self.assertIsInstance(serializer.page_size, int)

    def test_mount_user_payload(self):
        serializer = self.serializer(
            list_users=self.list_users, page_number=1, page_size=12
        )
        result = serializer._mount_user_payload(
            user=self.df.iloc[0], classification="NORMAL"
        )
        self.assertIsInstance(result, dict)
        self.assertEquals(result["type"], "NORMAL")
        self.assertEquals(result["gender"], "F")
        self.assertEquals(result["telephoneNumbers"][0], "+55154155648")
        self.assertEquals(result["mobileNumbers"][0], "+551082645550")

    def test_mount_list_users(self):
        serializer = self.serializer(
            list_users=self.list_users, page_number=1, page_size=12
        )
        list_users = serializer._mount_list_users()
        self.assertIsInstance(list_users, object)

    def test_create_message(self):
        serializer = self.serializer(
            list_users=self.list_users, page_number=1, page_size=12
        )
        message = serializer.create_message()
        self.assertIsInstance(message, dict)
