from locator.infra.repositories import LocatorRepo
from .iterators import SearchIterator, DataLoadIterator
from .validators import LocatorValidator
from .helpers import LocatorHelpers
from locator.infra.serializers import DefaultSerializer
from django.conf import settings
import redis, requests


class LocatorFactory:

    INPUT_CSV: str = "https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv"
    INPUT_JSON: str = "https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json"

    def create_search_iterator(self, data: dict) -> dict:
        """
        Create a Iterator to get a list of users
        :param data:
        :return: dict
        """

        return (
            SearchIterator(
                validator=LocatorValidator,
                repo=LocatorRepo,
                serializer=DefaultSerializer,
                redis=self.create_redis_instance(),
            )
            .set_params(search_payload=data)
            .execute()
        )

    def create_redis_instance(self):
        """
        Create a Redis instance to manipulate the redis storage
        :return: redis
        """

        return redis.StrictRedis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
        )

    def create_base_by_json(self, redis_instance) -> (str, Exception):
        """
        Create a Iterator to populate the redis with the data from json endpoint
        :param redis_instance:
        :return: str
        """
        return (
            DataLoadIterator(
                redis=redis_instance, requests=requests, helper=LocatorHelpers()
            )
            .set_params(url=self.INPUT_JSON, type_file="json")
            .execute()
        )

    def create_base_by_csv(self, redis_instance) -> (str, Exception):
        """
       Create a Iterator to populate the redis with the data from csv file
       :param redis_instance:
       :return: str
       """
        return (
            DataLoadIterator(
                redis=redis_instance, requests=requests, helper=LocatorHelpers()
            )
            .set_params(url=self.INPUT_CSV, type_file="csv")
            .execute()
        )
