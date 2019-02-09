#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from datetime import datetime

from Mocks import BaseReaderMock
from Working.TimeReaders import TimelineReader
from config import LOGGER


class Test(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testWennFuenfTageAbefragtWerdenDannWerdenFuenfTageErmittelt(self):
        with open("./resources/history-2018-01-01.kml", "r", encoding="utf-8") as f:
            url = f.read()
        timeline = TimelineReader(BaseReaderMock(url))
        actual = timeline.readTime(datetime(2017, 5, 3), datetime(2017, 5, 4))
        LOGGER.debug(len(actual.values()))
        LOGGER.debug(actual.values())
        assert len(actual.values()) == 2


# actual = reader.readTime(datetime(2017, 5, 5))
#         assert actual is not None


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
