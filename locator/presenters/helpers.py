from typing import Type
import phonenumbers as phn
import pandas as pd


class LocatorHelpers:
    @staticmethod
    def get_region(state: str) -> str:
        """ "
        Transform the range of dates in a string representation
        """
        state: str = state.title()
        region: str = ""
        states: dict = {
            "NORTE": [
                "Tocantins",
                "Pará",
                "Amapá",
                "Roraima",
                "Amazonas",
                "Acre",
                "Rondônia",
            ],
            "NORDESTE": [
                "Alagoas",
                "Bahia",
                "Ceará",
                "Maranhão",
                "Paraíba",
                "Pernambuco",
                "Piauí",
                "Rio Grande Do Norte",
                "Sergipe",
            ],
            "CENTRO-OESTE": [
                "Goiás",
                "Mato Grosso",
                "Mato Grosso Do Sul",
                "Distrito Federal",
            ],
            "SUDESTE": [
                "São Paulo",
                "Rio de Janeiro",
                "Espírito Santo",
                "Minas Gerais",
            ],
            "SUL": ["Rio Grande Do Sul", "Paraná", "Santa Catarina"],
        }

        for (key, values) in states.items():
            if state in values:
                region = key

        if not region:
            return "DESCONHECIDO"

        return region

    def _trasform_to_numeric(self, df: Type[pd.DataFrame], col: str) -> Type[pd.DataFrame]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        return df

    def _change_type_coordinates(self, df: Type[pd.DataFrame]) -> Type[pd.DataFrame]:
        df = self._trasform_to_numeric(df=df, col="location__coordinates__latitude")
        df = self._trasform_to_numeric(df=df, col="location__coordinates__longitude")
        return df

    def _set_col_phonenumber(self, df: Type[pd.DataFrame], col: str) -> Type[pd.DataFrame]:
        df[col] = df[col].apply(
            lambda x: phn.format_number(phn.parse(x, "BR"), phn.PhoneNumberFormat.E164)
        )
        return df

    def _change_phones_number(self, df: Type[pd.DataFrame]) -> Type[pd.DataFrame]:
        df = self._set_col_phonenumber(df=df, col="phone")
        df = self._set_col_phonenumber(df=df, col="cell")
        return df

    def _remove_cols_dataframe(self, df: Type[pd.DataFrame], cols: list = ["dob__age", "registered__age"]) -> Type[pd.DataFrame]:
        return df.drop(cols, axis=1)

    def _change_col_gender(self, df: Type[pd.DataFrame]) -> Type[pd.DataFrame]:
        df["gender"] = df.gender.apply(lambda x: "F" if x == "female" else "M")
        return df

    def format_dataframe(self, df: Type[pd.DataFrame]) -> Type[pd.DataFrame]:
        df = self._remove_cols_dataframe(df=df)
        df = self._change_col_gender(df=df)
        df = self._change_phones_number(df=df)
        df = self._change_type_coordinates(df=df)

        return df
