#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import time

import numpy
from pandas.core.frame import DataFrame
from pandas.core.series import Series

from Env.TimeConstants import GOOGLE
from Env.Utils import TimesFormatter
from Framing.Common import FrameBuilder
from config import LOGGER


class PauseDurationBuilder(FrameBuilder):

    def _build_data(self, df: DataFrame) -> DataFrame:
        def set_pause(row):
            return self.__set_pause(row)

        return self._call_each_row(df, set_pause)

    def __set_pause(self, row):
        begin = row[GOOGLE.BeginTime]
        if not isinstance(begin, time):
            begin = begin.get(GOOGLE.BeginTime, -1)
        end = row[GOOGLE.EndTime]
        if not isinstance(end, time):
            end = end.get(GOOGLE.EndTime, -1)
        dur = TimesFormatter.calculate_duration(begin,
                                                end)
        old_dur = row[GOOGLE.Duration]
        if isinstance(old_dur, Series):
            old_dur = old_dur.get(GOOGLE.Duration, -1)
        row[GOOGLE.Pause] = dur - old_dur
        return row


class WorkplaceBuilder(FrameBuilder):

    def __init__(self, places_to_work: dict):

        super(WorkplaceBuilder, self).__init__()
        LOGGER.info("Arbeitsplätze: " + str(places_to_work))
        if len(places_to_work.keys()) == 0:
            raise ValueError("Keine Arbeitsplätze vorhanden")
        self.places_to_work = places_to_work

    def _build_data(self, df: DataFrame) -> DataFrame:
        df = self._add_column(df, GOOGLE.Workplace, df[GOOGLE.Name])

        def mark_work(x):
            return self.__mark_work(x)

        return self._call_each_row(df, mark_work)

    def __is_workplace(self, row, workplaces):
        name = row[GOOGLE.Name]
        adress = row[GOOGLE.Address]
        if not isinstance(adress, str) and numpy.isnan(adress):
            adress = None
        is_work = False
        for work in workplaces:
            text: str = str(work)
            if (name and name.find(text) > -1) or \
                    (adress and adress.find(text) > -1):
                is_work = True
                break
        return is_work

    def __mark_work(self, row):
        for elem in self.places_to_work:
            item = elem
            workplaces: list = self.places_to_work.get(item)
            is_workplace = self.__is_workplace(row, workplaces)
            if is_workplace:
                value = str(item)
                LOGGER.info("Der Arbeitsplatz " + value +
                            " wurde gefunden")
                row[GOOGLE.Workplace] = value
                break
            else:
                row[GOOGLE.Workplace] = ""
        return row
