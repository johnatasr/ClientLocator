from dataclasses import dataclass
from typing import Type


@dataclass()
class Name:
    title: str
    first: str
    last: str


@dataclass()
class Coordinates:
    latitude: float
    longitude: float


@dataclass()
class Timezone:
    offset: str
    description: str


@dataclass()
class Location:
    region: str
    street: str
    city: str
    state: str
    postcode: str
    coordinates: Type[Coordinates]
    timezone: Type[Timezone]


@dataclass()
class Picture:
    large: str
    medium: str
    thumbnail: str


@dataclass()
class User:
    type_classfication: str
    gender: str
    name: Type[Name]
    location: Type[Location]
    email: str
    registered: str
    birthday: str
    telephone_numbers: list
    mobile_numbers: list
    picture: Type[Picture]
    nationality: str
