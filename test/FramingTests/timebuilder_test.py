#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from datetime import datetime, time

from pandas.core.frame import DataFrame

from Env.TimeConstants import GOOGLE
from Framing.Common import FrameBuilder, TimeBuilder
from config import LOGGER


class TimeBuilderTest(unittest.TestCase):


    def createBuilder(self, date) -> FrameBuilder:
        return TimeBuilder(date, 0)

    def setUp(self):
        self.df: DataFrame = DataFrame({GOOGLE.BeginDate: '2000-01-01T10:30:00.000Z',GOOGLE.EndDate:
                                                           '2000-01-01T11:59:00.000Z'},[1,2])

    def tearDown(self):
        pass

    def testBuildFrame(self):
        builder = self.createBuilder(datetime(2000, 1, 1))

        df = builder.build_frame(self.df)

        LOGGER.debug(df.to_string())
        assert GOOGLE.BeginDate in df.columns
        assert GOOGLE.EndDate in df.columns
        assert GOOGLE.BeginTime in df.columns
        assert GOOGLE.EndTime in df.columns
        assert GOOGLE.Duration in df.columns

    def testDateBuildFrame(self):
        builder = self.createBuilder(datetime(2000, 1, 1))

        df: DataFrame = builder.build_frame(self.df)
        begin=df[GOOGLE.BeginDate]
        self.assertEqual(begin.get_values()[0],
                         datetime(2000, 1, 1).date(), "")
        self.assertEqual(df[GOOGLE.EndDate].get_values()[0],
                         datetime(2000, 1, 1).date(), "")

    def testTimeBuildFrame(self):
        builder = self.createBuilder(datetime(2000, 1, 1))

        df: DataFrame = builder.build_frame(self.df)

        LOGGER.debug(df.to_string())
        self.assertEqual(df[GOOGLE.BeginTime].get_values()[0],
                         time(10, 30), "msg")
        self.assertEqual(df[GOOGLE.EndTime].get_values()[0], time(12), "")

    def testDurationBuildFrame(self):
        builder = self.createBuilder(datetime(2000, 1, 1))

        df = builder.build_frame(self.df)

        LOGGER.debug(df.to_string())
        self.assertEqual(df[GOOGLE.Duration].get_values()[0], 90)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
