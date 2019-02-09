#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from datetime import datetime, time

from Env.Utils import TimesFormatter
from config import LOGGER
from dateutil import tz


class TimesFormatterTest(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_roundTime_WennDerOperatorPlusIst_DannRundeAuf(self):
        inputarg = TimesFormatter.convertTimezone(
                datetime(2013, 5, 5, 2, 5, tzinfo=tz.tzlocal()))
        output = TimesFormatter.convertTimezone(
                datetime(2013, 5, 5, 2, 15, tzinfo=tz.tzlocal()))
        res = TimesFormatter.roundTime(
                inputarg)
        LOGGER.debug("Ergebnis: " + str(res) + " Input: " + str(inputarg))
        assert res == output

    def test_roundTime_WennDerOperatorMinusIst_DannRundeAb(self):
        inputarg = TimesFormatter.convertTimezone(
                datetime(2013, 5, 5, 2, 5, tzinfo=tz.tzlocal()))
        output = TimesFormatter.convertTimezone(
                datetime(2013, 5, 5, 2, 0, tzinfo=tz.tzlocal()))
        res = TimesFormatter.roundTime(
                inputarg, shiftOp="-")
        LOGGER.debug("Ergebnis: Output" + str(res) +
                     " Input: " + str(inputarg))
        assert res == output

    def test_dur(self):
        b_time = TimesFormatter.convertTimezone(
                datetime(2013, 5, 5, 2, 10, tzinfo=tz.tzlocal()))
        e_time = TimesFormatter.convertTimezone(
                datetime(2013, 5, 5, 2, 46, tzinfo=tz.tzlocal()))
        res = TimesFormatter.calculateDuration(b_time, e_time)
        LOGGER.debug("Ergebnis: " + str(res))
        assert res == 36

    def test_durstr(self):
        res = TimesFormatter.toDurationString(90)
        LOGGER.debug("Ergebnis: " + str(res))
        assert res == "01:30"

    def test_durstr2(self):
        res = TimesFormatter.calculateDuration(time(1, 1), time(1, 1))
        LOGGER.debug("Ergebnis: " + str(res))
        assert res == 0


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
