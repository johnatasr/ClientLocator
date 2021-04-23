from clientlocator.exceptions import InteratorException
from locator.infra.interfaces import IIterator
from typing import Any
import pyarrow as pa
import pandas as pd
import json


"""
  In Iterators occour all iteration beetween repositories, serializers and validators
  adding the business rules in process
"""


class SearchIterator(IIterator):
    """ "
    Interactor responsible for search a list of users, called by API
    """

    def __init__(self, validator=None, repo=None, serializer=None, redis=None):
        """
           Starts the iterator with the depedencies
           :param validator: LocatorValidator
           :param repo: LocatorRepo
           :param serializer: DefaultSerializer
           :param redis: redis
           :return: None
        """
        self.validator: object = validator
        self.serializer: object = serializer
        self.redis = redis
        self.repo: object = repo(redis_instance=self.redis)

    def set_params(self, search_payload: dict):
        """
           Params to manipulation in execute
           :param search_payload: dict
           :return: SearchIterator
        """
        self.payload = search_payload
        return self

    def execute(self):
        """
          All execution is done in this method, in the case, get a list of users
          :return: dict
        """
        try:
            valided_payload = self.validator().validate_payload(self.payload)

            if valided_payload:
                latitude: float = self.payload["coordinates"]["lat"]
                longitude: float = self.payload["coordinates"]["lon"]
                page_number: int = self.payload["pageNumber"]
                page_size: int = self.payload["pageSize"]

                list_users: Any = self.repo.get_clients_by_position(
                    lat=latitude, lon=longitude
                )

                if isinstance(list_users, str):
                    return {"msg": list_users}

                serialized_return: dict = self.serializer(
                    list_users=list_users, page_number=page_number, page_size=page_size
                ).create_message()

                return serialized_return
        except InteratorException as error:
            raise InteratorException(error)


class DataLoadIterator(IIterator):
    """ "
    Iteractor responsible for manipulate all process of insert data in Redis
    """

    def __init__(self, redis=None, requests=None, helper=None):
        """
          Starts the iterator with the depedencies
          :param helper: LocatorHelper
          :param requests: requests
          :param redis: redis
          :return: None
        """
        self.redis = redis
        self.requests = requests
        self.helper = helper

    def set_params(self, url: str, type_file: str):
        """
           Params to manipulation in execute
           :param url: str
           :param type_file: str
           :return: DataLoadIterator
        """
        self.url = url
        self.type_file = type_file
        return self

    def execute(self):
        """
          All execution is done in this method, in the case, populate Redis with data
          :return: str
        """
        try:
            if self.type_file == "json":
                request = self.requests.get(self.url)
                request_data = json.loads(request.text)
                df = self._create_dataframe_from_json(data=request_data["results"])
                df = self._format_dataframe(df=df)
                self._set_redis(key="json-populate", df=df)

            if self.type_file == "csv":
                df = self._create_dataframe_from_csv(url=self.url)
                df = self._format_dataframe(df=df)
                self._set_redis(key="csv-populate", df=df)

            return "Base import successful"

        except InteratorException as error:
            raise InteratorException(error)

    def _create_dataframe_from_json(self, data: dict):
        return pd.json_normalize(data, sep="__")

    def _create_dataframe_from_csv(self, url: str):
        return pd.read_csv(url)

    def _format_dataframe(self, df):
        return self.helper.format_dataframe(df=df)

    def _set_redis(self, key: str = None, df=None):
        context = pa.default_serialization_context()
        self.redis.set(key, context.serialize(df).to_buffer().to_pybytes())
