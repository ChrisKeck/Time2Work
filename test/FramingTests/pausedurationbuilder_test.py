#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from datetime import time

from pandas.core.frame import DataFrame

from Env.TimeConstants import GOOGLE
from Framing.Custom import PauseDurationBuilder


class PauseDurationBuilderTest(unittest.TestCase):

    def setUp(self):
        self.df = DataFrame({GOOGLE.BeginTime: [time(10)],
                             GOOGLE.EndTime: [time(13)],
                             GOOGLE.Duration: [60],
                             GOOGLE.Pause: [0]})

    def tearDown(self):
        pass

    def testName(self):
        builder = PauseDurationBuilder()
        df = builder.build_frame(self.df)
        assert df[GOOGLE.Pause][0] == 120


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
