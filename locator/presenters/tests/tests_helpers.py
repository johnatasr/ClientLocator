from locator.presenters.iterators import DataLoadIterator
from locator.presenters.factories import LocatorFactory
from locator.presenters.helpers import LocatorHelpers
from django.test import TestCase


class LocatorHelpersTestCase(TestCase):
    """
    Tests of LocatorHelpers in locator.presenters.helpers.py
    """

    def setUp(self):
        INPUT_CSV: str = "https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv"

        self.helpers = LocatorHelpers()
        self.iterator = DataLoadIterator(
            redis=LocatorFactory().create_redis_instance(), helper=LocatorHelpers()
        )
        self.df = self.iterator._create_dataframe_from_csv(INPUT_CSV)

    def test_get_region(self):
        region: str = self.helpers.get_region(state="ceará")
        self.assertIsInstance(region, str)
        self.assertEquals(region, "NORDESTE")

    def test_get_region_fail(self):
        region: str = self.helpers.get_region(state="new york")
        self.assertIsInstance(region, str)
        self.assertEquals(region, "DESCONHECIDO")

    def test_transform_to_numeric(self):
        df = self.helpers._trasform_to_numeric(
            df=self.df, col="location__coordinates__latitude"
        )
        self.assertIsInstance(df.iloc[0]["location__coordinates__latitude"], float)

    def test_change_type_coordinates(self):
        df = self.helpers._change_type_coordinates(df=self.df)
        self.assertIsInstance(df.iloc[0]["location__coordinates__latitude"], float)
        self.assertIsInstance(df.iloc[0]["location__coordinates__longitude"], float)

    def test_set_col_phonenumber(self):
        df = self.helpers._set_col_phonenumber(df=self.df, col="phone")
        self.assertEquals(df.iloc[0]["phone"], "+55154155648")

    def test_change_phones_number(self):
        df = self.helpers._set_col_phonenumber(df=self.df, col="phone")
        df = self.helpers._set_col_phonenumber(df=df, col="cell")
        self.assertEquals(df.iloc[0]["phone"], "+55154155648")
        self.assertEquals(df.iloc[0]["cell"], "+551082645550")

    def test_remove_cols_dataframe(self):
        df = self.helpers._remove_cols_dataframe(df=self.df)
        self.assertEquals("dob__age" not in df.columns, True)
        self.assertEquals("registered__age" not in df.columns, True)

    def test_change_col_gender(self):
        df = self.helpers._change_col_gender(df=self.df)
        self.assertEquals(df.iloc[0]["gender"], "F")
