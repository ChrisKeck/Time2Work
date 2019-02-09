#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from datetime import datetime, time

from Env.TimeConstants import BA
from Framing.Specifics import BAFormatFinalizer
from config import LOGGER
from pandas.core.frame import DataFrame


class BAFormatFinalizerTest(unittest.TestCase):


    def setUp(self):
        self.df = DataFrame({BA.Duration: [59, 0],
                             BA.Pause: [305, 80],
                             BA.BeginTime: [time(12, 15), time(13, 15)],
                             BA.EndTime: [time(15, 15), time(16, 15)],
                             BA.BuildDate: [datetime(2000, 1, 1).date(),
                                            datetime(2022, 1, 1).date()]})

    def tearDown(self):
        pass

    def testName(self):
        builder = BAFormatFinalizer()
        df = builder.buildFrame(self.df)
        LOGGER.info(df)
        assert df.get_value(0, BA.Duration) == "01:00"

    def testName2(self):
        builder = BAFormatFinalizer()
        df = builder.buildFrame(self.df)
        LOGGER.info(df)
        assert df.get_value(0, BA.Pause) == "05:15"

    def testName3(self):
        builder = BAFormatFinalizer()
        df = builder.buildFrame(self.df)
        LOGGER.info(df)
        assert df.get_value(0, BA.BuildDate) == "01.01.2000"

    def testName4(self):
        builder = BAFormatFinalizer()
        df = builder.buildFrame(self.df)
        LOGGER.info(df)
        assert df.get_value(0, BA.BeginTime) == "12:15"


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
