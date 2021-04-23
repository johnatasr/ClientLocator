from dataclasses import dataclass
from typing import Type
import pandas as pd


@dataclass(unsafe_hash=True)
class ListUsers:
    classification: object
    users: Type[pd.DataFrame]

    def __repr__(self):
        return f"Entity: {self.__class__.__name__}<>"
