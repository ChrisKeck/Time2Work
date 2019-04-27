#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from datetime import datetime, time

from dateutil import tz

from Env.Utils import TimesFormatter
from config import LOGGER


class TimesFormatterTest(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_roundTime_WennDerOperatorPlusIst_DannRundeAuf(self):
        inputarg = TimesFormatter.convert_timezone(
                datetime(2013, 5, 5, 2, 5, tzinfo=tz.tzlocal()))
        output = TimesFormatter.convert_timezone(
                datetime(2013, 5, 5, 2, 15, tzinfo=tz.tzlocal()))
        res = TimesFormatter.round_time(
                inputarg)
        LOGGER.debug("Ergebnis: " + str(res) + " Input: " + str(inputarg))
        assert res == output

    def test_roundTime_WennDerOperatorMinusIst_DannRundeAb(self):
        inputarg = TimesFormatter.convert_timezone(
                datetime(2013, 5, 5, 2, 5, tzinfo=tz.tzlocal()))
        output = TimesFormatter.convert_timezone(
                datetime(2013, 5, 5, 2, 0, tzinfo=tz.tzlocal()))
        res = TimesFormatter.round_time(
                inputarg, "-")
        LOGGER.debug("Ergebnis: Output" + str(res) +
                     " Input: " + str(inputarg))
        assert res == output

    def test_dur(self):
        b_time = TimesFormatter.convert_timezone(
                datetime(2013, 5, 5, 2, 10, tzinfo=tz.tzlocal()))
        e_time = TimesFormatter.convert_timezone(
                datetime(2013, 5, 5, 2, 46, tzinfo=tz.tzlocal()))
        res = TimesFormatter.calculate_duration(b_time, e_time)
        LOGGER.debug("Ergebnis: " + str(res))
        assert res == 36

    def test_durstr(self):
        res = TimesFormatter.to_duration_string(90)
        LOGGER.debug("Ergebnis: " + str(res))
        assert res == "01:30"

    def test_durstr2(self):
        res = TimesFormatter.calculate_duration(time(1, 1), time(1, 1))
        LOGGER.debug("Ergebnis: " + str(res))
        assert res == 0


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
