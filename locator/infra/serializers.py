from locator.infra.interfaces import ISerializer
from django.core.paginator import Paginator
from locator.presenters.helpers import LocatorHelpers
from typing import Type
import pandas as pd


class DefaultSerializer(ISerializer):
    def __init__(self, list_users: object, page_number: int, page_size: int):
        self.list_users = list_users
        self.page_number = page_number
        self.page_size = page_size
        self.helper = LocatorHelpers()

    def _mount_user_payload(
        self, user: Type[pd.DataFrame], classification: str
    ) -> dict:
        payload: dict = {
            "type": classification,
            "gender": user["gender"],
            "name": {
                "title": user["name__title"],
                "first": user["name__first"],
                "last": user["name__last"],
            },
            "location": {
                "region": self.helper.get_region(state=user["location__state"]),
                "street": user["location__street"],
                "city": user["location__city"],
                "state": user["location__state"],
                "postcode": user["location__postcode"],
                "coordinates": {
                    "latitude": user["location__coordinates__latitude"],
                    "longitude": user["location__coordinates__longitude"],
                },
                "timezone": {
                    "offset": user["location__timezone__offset"],
                    "description": user["location__timezone__description"],
                },
            },
            "email": user["email"],
            "registered": user["registered__date"],
            "birthday": user["dob__date"],
            "telephoneNumbers": [
                user["phone"],
            ],
            "mobileNumbers": [user["cell"]],
            "picture": {
                "large": user["picture__large"],
                "medium": user["picture__medium"],
                "thumbnail": user["picture__thumbnail"],
            },
            "nationality": "BR"
            if user["phone"].split("+")[1][0:2] == "55"
            else "OTHER",
        }

        return payload

    def _paginate_list_users(self, users: list) -> object:
        paginated_users = Paginator(users, self.page_size)

        if len(users) < self.page_size:
            self.page_number = 1

        page_users = paginated_users.page(self.page_number)
        return page_users

    def _mount_list_users(self) -> list:
        users: list = list()
        classification: str = self.list_users.classification.name

        for index, user in self.list_users.users.iterrows():
            usr: dict = self._mount_user_payload(
                user=user, classification=classification
            )
            users.append(usr)

        users: Type[Paginator] = self._paginate_list_users(users)

        return users

    def mount_payload(self) -> dict:
        users: Type[Paginator] = self._mount_list_users()

        return {
            "pageNumber": self.page_number,
            "pageSize": self.page_size,
            "totalCount": len(users),
            "users": users.object_list,
        }

    def create_message(self) -> dict:
        message: dict = self.mount_payload()
        return message
