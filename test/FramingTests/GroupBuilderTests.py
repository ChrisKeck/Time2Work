#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from datetime import datetime

from Env.TimeConstants import GOOGLE
from Framing.Grouping import DurationGroupBuilder
from pandas.core.frame import DataFrame


class Test(unittest.TestCase):


    def setUp(self):
        self.df = DataFrame(
                {GOOGLE.BuildDate: [datetime(2000, 1, 1).date(),
                                    datetime(2000, 1, 1).date()],
                 GOOGLE.BeginDate: [datetime(2000, 1, 1).date(),
                                    datetime(2000, 1, 1).date()],
                 GOOGLE.BeginTime: [datetime(2000, 1, 1, 12, 30).time(),
                                    datetime(2000, 1, 1, 17).time()],
                 GOOGLE.EndDate: [datetime(2000, 1, 1).date(),
                                  datetime(2000, 1, 1).date()],
                 GOOGLE.EndTime: [datetime(2000, 1, 1, 13, 30).time(),
                                  datetime(2000, 1, 1, 18).time()],
                 GOOGLE.Workplace: ["ISO", "ISO"],
                 GOOGLE.Duration: [100, 150]})

    def tearDown(self):
        pass

    def appendRows(self, df):
        additional = DataFrame(
                {GOOGLE.BuildDate: [datetime(2000, 1, 1).date(),
                                    datetime(2000, 1, 1).date()],
                 GOOGLE.BeginDate: [datetime(2000, 1, 1).date(),
                                    datetime(2000, 1, 1).date()],
                 GOOGLE.BeginTime: [datetime(2000, 1, 1, 18, 15).time(),
                                    datetime(2000, 1, 1, 19, 15).time()],
                 GOOGLE.EndDate: [datetime(2000, 1, 1).date(),
                                  datetime(2000, 1, 1).date()],
                 GOOGLE.EndTime: [datetime(2000, 1, 1, 19).time(),
                                  datetime(2000, 1, 1, 20).time()],
                 GOOGLE.Workplace: ["Test", "ISO"],
                 GOOGLE.Duration: [100, 150]})
        df = df.append(additional)
        return df

    def testName(self):
        df = self.appendRows(self.df)
        builder = self.createDurationBuilderGroup(["ISO"])
        df = builder.buildFrame(df)
        dur = df[GOOGLE.Duration].get_values()[0]
        assert dur == 400

    def testName2(self):
        builder = self.createDurationBuilderGroup(["ISO"])
        df = builder.buildFrame(self.df)
        dur = df[GOOGLE.Duration].get_values()[0]
        assert dur == 250

    def createDurationBuilderGroup(self, places: list):
        return DurationGroupBuilder(places)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
