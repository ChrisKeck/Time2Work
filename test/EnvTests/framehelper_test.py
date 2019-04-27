#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from pandas.core.frame import DataFrame

from Env.TimeConstants import GOOGLE
from Env.Utils import ColumnsWorker


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_WennSpaltenHinzugefuegtWurden_DannSindSieImFrameEnthalten(self):
        df = DataFrame()
        df = ColumnsWorker.add_columns(GOOGLE, df)
        assert len(df.columns) > 0

    def test_Name(self):
        df = DataFrame({"Test1": [1, 2], "Test2": ["1", "2"]})
        df = ColumnsWorker.add_column(df, "Test3", "value")
        test3Values = df["Test3"].get_values()
        isValid = "value" in test3Values
        print(test3Values.__class__)
        print(test3Values)
        assert isValid

    def test_Name3(self):
        df = DataFrame({"Test1": [1, 2], "Test2": ["1", "2"]})
        df = ColumnsWorker.add_column(df, "Test3", df["Test2"])
        test3Values = df["Test3"].get_values()
        isValid = "1" in test3Values and "2" in test3Values
        print(test3Values.__class__)
        print(test3Values)
        assert isValid

    def test_Name4(self):
        df = DataFrame({"Test1": [1, 2], "Test2": [
            "1", "2"], "Test3": ["1", "2"]})
        df = ColumnsWorker.drop_columns(df, ["Test2"])
        isValid = "Test1" in df and "Test3" in df and "Test2" not in df
        assert isValid

    def test_Name5(self):
        df = DataFrame({"Test1": [1, 2], "Test2": [
            "1", "2"], "Test3": ["1", "2"]})
        lst = ColumnsWorker.get_columns_in_frame(df, ["Test2"])
        isValid = "Test2" in lst and len(lst) == 1
        assert isValid

    def test_Name6(self):
        df = DataFrame({"Test1": [1, 2], "Test2": [
            "1", "2"], "Test3": ["1", "2"]})
        df = ColumnsWorker.reassign_columns(df, ["Test3", "Test2"])
        print(df)
        isValid = "Test3" == df.columns[0] and "Test2" == df.columns[1] and "Test1" not in df
        assert isValid

    def test_Name7(self):
        df = DataFrame({"Test1": [1, 2], "Test2": [
            "1", "2"], "Test3": ["1", "2"]})
        df = ColumnsWorker.rename_columns(df, {"Test3": "3Test"})
        print(df)
        isValid = "Test3" not in df and "3Test" in df and "Test1" in df and "Test2" in df
        assert isValid

    def test_Name8(self):
        df = DataFrame({"Test1": [1, 2], "Test2": [
            "1", "2"], "Test3": ["1", "2"]})
        df = ColumnsWorker.rename_columns(df, {"Test3": "Test1"})
        print(df)
        isValid = "Test3" not in df and "Test1" in df and \
                  "Test2" in df and "1" in df["Test1"].get_values()
        assert isValid


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
