from django.test import TestCase
from locator.presenters.iterators import (
    SearchIterator,
    DataLoadIterator,
)
from locator.presenters.factories import LocatorFactory
from locator.presenters.validators import LocatorValidator
from locator.presenters.helpers import LocatorHelpers
from locator.infra.repositories import LocatorRepo
from locator.infra.serializers import DefaultSerializer
from typing import Type
import requests
import json
import pandas as pd


class SearchIteratorTestCase(TestCase):
    """
    Tests of SearchIterator in locator.presenters.iterator.py
    """

    def setUp(self):
        self.iterator = SearchIterator(
            validator=LocatorValidator,
            repo=LocatorRepo,
            serializer=DefaultSerializer,
            redis=LocatorFactory().create_redis_instance(),
        )

        self.data: dict = {
            "pageNumber": 1,
            "pageSize": 10,
            "coordinates": {"lat": -38.9614, "lon": -10.766959},
        }

    def test_init(self):
        self.assertIsInstance(self.iterator, object)
        self.assertIsInstance(self.iterator.validator, object)
        self.assertIsInstance(self.iterator.repo, object)
        self.assertIsInstance(self.iterator.serializer, object)
        self.assertIsInstance(self.iterator.redis, object)

    def test_set_params(self):
        self.iterator.set_params(search_payload=self.data)
        self.assertIsInstance(self.iterator.payload, dict)
        self.assertEquals(self.iterator.payload["pageNumber"], 1)
        self.assertEquals(self.iterator.payload["pageSize"], 10)
        self.assertEquals(self.iterator.payload["coordinates"]["lat"], -38.9614)
        self.assertEquals(self.iterator.payload["coordinates"]["lon"], -10.766959)

    def test_execute(self):
        result = self.iterator.set_params(search_payload=self.data).execute()
        self.assertIsInstance(result, dict)


class DataLoadIteratorTestCase(TestCase):
    """
    Tests of DataLoadIterator in locator.presenters.iterator.py
    """

    INPUT_CSV: str = "https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv"
    INPUT_JSON: str = "https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json"

    def setUp(self):
        self.iterator = DataLoadIterator(
            redis=LocatorFactory().create_redis_instance(),
            requests=requests,
            helper=LocatorHelpers(),
        )

    def test_init(self):
        self.assertIsInstance(self.iterator, object)
        self.assertIsInstance(self.iterator.redis, object)
        self.assertIsInstance(self.iterator.requests, object)
        self.assertIsInstance(self.iterator.helper, object)

    def test_set_params_csv(self):
        self.iterator.set_params(url=self.INPUT_CSV, type_file="csv")
        self.assertIsInstance(self.iterator.url, str)
        self.assertEquals(self.iterator.url, self.INPUT_CSV)
        self.assertIsInstance(self.iterator.type_file, str)
        self.assertEquals(self.iterator.type_file, "csv")

    def test_set_params_json(self):
        self.iterator.set_params(url=self.INPUT_JSON, type_file="json")
        self.assertIsInstance(self.iterator.url, str)
        self.assertEquals(self.iterator.url, self.INPUT_JSON)
        self.assertIsInstance(self.iterator.type_file, str)
        self.assertEquals(self.iterator.type_file, "json")

    def test_execute_csv(self):
        result = self.iterator.set_params(url=self.INPUT_CSV, type_file="csv").execute()
        self.assertIsInstance(result, str)
        self.assertEquals(result, "Base import successful")

    def test_execute_json(self):
        result = self.iterator.set_params(
            url=self.INPUT_JSON, type_file="json"
        ).execute()
        self.assertIsInstance(result, str)
        self.assertEquals(result, "Base import successful")

    def test_create_dataframe_from_json(self):
        request = self.iterator.requests.get(self.INPUT_JSON)
        request_data = json.loads(request.text)
        df = self.iterator._create_dataframe_from_json(data=request_data["results"])
        self.assertIsInstance(df, object)

    def test_create_dataframe_from_csv(self):
        df = self.iterator._create_dataframe_from_csv(self.INPUT_CSV)
        self.assertIsInstance(df, object)

    def test_format_dataframe(self):
        df = self.iterator._create_dataframe_from_csv(self.INPUT_CSV)
        formated_df = self.iterator._format_dataframe(df=df)
        row_1 = formated_df.iloc[0]
        self.assertEquals(row_1["gender"], "F")
        self.assertEquals(row_1["phone"], "+55154155648")
