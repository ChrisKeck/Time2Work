#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from Env.TimeConstants import GOOGLE
from Env.Utils import ColumnsWorker
from pandas.core.frame import DataFrame


class Test(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testWennSpaltenHinzugefuegtWurden_DannSindSieImFrameEnthalten(self):
        df = DataFrame()
        df = ColumnsWorker.addColumns(GOOGLE, df)
        assert len(df.columns) > 0

    def testName(self):
        df = DataFrame({"Test1": [1, 2], "Test2": ["1", "2"]})
        df = ColumnsWorker.addColumn(df, "Test3", "value")
        test3Values = df["Test3"].get_values()
        isValid = "value" in test3Values
        print(test3Values.__class__)
        print(test3Values)
        assert isValid

    def testName3(self):
        df = DataFrame({"Test1": [1, 2], "Test2": ["1", "2"]})
        df = ColumnsWorker.addColumn(df, "Test3", df["Test2"])
        test3Values = df["Test3"].get_values()
        isValid = "1" in test3Values and "2" in test3Values
        print(test3Values.__class__)
        print(test3Values)
        assert isValid

    def testName4(self):
        df = DataFrame({"Test1": [1, 2], "Test2": [
            "1", "2"], "Test3": ["1", "2"]})
        df = ColumnsWorker.dropColumns(df, ["Test2"])
        isValid = "Test1" in df and "Test3" in df and "Test2" not in df
        assert isValid

    def testName5(self):
        df = DataFrame({"Test1": [1, 2], "Test2": [
            "1", "2"], "Test3": ["1", "2"]})
        lst = ColumnsWorker.getColumnsInFrame(df, ["Test2"])
        isValid = "Test2" in lst and len(lst) == 1
        assert isValid

    def testName6(self):
        df = DataFrame({"Test1": [1, 2], "Test2": [
            "1", "2"], "Test3": ["1", "2"]})
        df = ColumnsWorker.reassignColumns(df, ["Test3", "Test2"])
        print(df)
        isValid = "Test3" == df.columns[0] and "Test2" == df.columns[1] and "Test1" not in df
        assert isValid

    def testName7(self):
        df = DataFrame({"Test1": [1, 2], "Test2": [
            "1", "2"], "Test3": ["1", "2"]})
        df = ColumnsWorker.renameColumns(df, {"Test3": "3Test"})
        print(df)
        isValid = "Test3" not in df and "3Test" in df and "Test1" in df and "Test2" in df
        assert isValid

    def testName8(self):
        df = DataFrame({"Test1": [1, 2], "Test2": [
            "1", "2"], "Test3": ["1", "2"]})
        df = ColumnsWorker.renameColumns(df, {"Test3": "Test1"})
        print(df)
        isValid = "Test3" not in df and "Test1" in df and \
                  "Test2" in df and "1" in df["Test1"].get_values()
        assert isValid


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
