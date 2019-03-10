#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from Working.FrameCollectors import FrameCollector


def readFile():
    with open("/home/kec/IdeaProjects/Time2Work/resources/history-2018-01-01.kml", "r", encoding="utf-8") as f:
        url = f.read()
    return url


class DataFrameBuilderTest(unittest.TestCase):

    def setUp(self):
        self.url = readFile()

    def tearDown(self):
        pass

    def test_wenn_nicht_(self):
        collector = FrameCollector()
        df = collector.build(self.url)
        assert not df.empty


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
