from clientlocator.exceptions import ConflictException
from locator.presenters.helpers import LocatorHelpers
from locator.domain.entities import (
    classification as clsn,
    list_users as lu,
)
from typing import Type
from dataclasses import dataclass
import pandas as pd
import pyarrow as pa


class LocatorRepo:
    """
    This layer is responsible for interacting with models and entities
    """

    helper: Type[LocatorHelpers] = LocatorHelpers()

    def __init__(self, redis_instance):
        self.redis = redis_instance

    def get_clients_by_position(self, lat: float, lon: float) -> (dict, str):
        """
        Get a list of Clients by coordinates
        """
        try:
            classification: Type[clsn.Classification] = self.create_classification(
                lat=lat, lon=lon
            )
            classification.get_classification()

            df: Type[pd.DataFrame] = self.get_all_data()

            df = df[
                df["location__coordinates__latitude"].between(
                    classification.minlat, classification.maxlat
                )
                & df["location__coordinates__longitude"].between(
                    classification.maxlon, classification.minlon
                )
            ]

            if df.empty:
                return (
                    f"No clients found with coordinates: "
                    f"Lattitude;{lat}, Longitude:{lon}"
                )

            list_users: Type[lu.ListUsers] = self.create_list_users(
                classification=classification, users=df
            )

            return list_users

        except ConflictException as err:
            raise ConflictException(
                source="repository",
                code="conflit_get_all_clients",
                message=f"Error in load clients by position: {err}",
            )

    def get_all_data(self) -> Type[pd.DataFrame]:
        """
        Get all data in Redis
        """
        try:
            context = pa.default_serialization_context()
            json_df = context.deserialize(self.redis.get("json-populate"))
            csv_df = context.deserialize(self.redis.get("csv-populate"))
            dfs = [json_df, csv_df]
            return pd.concat(dfs)
        except ConflictException as err:
            raise ConflictException(
                source="repository",
                code="conflit_get_all_data",
                message=f"Error in get all data in Redis: {err}",
            )

    def create_classification(self, lat: float, lon: float) -> Type[dataclass]:
        """
        Create a Classification Entity
        """
        try:
            return clsn.Classification(lat=lat, lon=lon)
        except ConflictException as err:
            raise ConflictException(
                source="repository",
                code="conflit_in_create",
                message=f"Error in create a Classification Entity: {err}",
            )

    def create_list_users(
        self, classification: Type[clsn.Classification], users: Type[pd.DataFrame]
    ) -> Type[dataclass]:
        """
        Create a ListUsers Entity
        """
        try:
            return lu.ListUsers(classification=classification, users=users)
        except ConflictException as err:
            raise ConflictException(
                source="repository",
                code="conflit_in_create",
                message=f"Error in create a ListUsers Entity: {err}",
            )
