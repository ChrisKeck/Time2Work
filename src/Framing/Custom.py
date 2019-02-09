#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import time

import numpy
from Env.TimeConstants import GOOGLE
from Env.Utils import TimesFormatter
from Framing.Common import FrameBuilder
from config import LOGGER
from pandas.core.frame import DataFrame
from pandas.core.series import Series


class PauseDurationBuilder(FrameBuilder):


    def _build_Data(self, df) -> DataFrame:
        def setPause(row):
            return self.__setPause(row)

        return self._callEachRow(df, setPause)

    def __setPause(self, row):
        begin = row[GOOGLE.BeginTime]
        if not isinstance(begin, time):
            begin = begin.get(GOOGLE.BeginTime, -1)
        end = row[GOOGLE.EndTime]
        if not isinstance(end, time):
            end = end.get(GOOGLE.EndTime, -1)
        dur = TimesFormatter.calculateDuration(begin,
                                               end)
        oldDur = row[GOOGLE.Duration]
        if isinstance(oldDur, Series):
            oldDur = oldDur.get(GOOGLE.Duration, -1)
        row[GOOGLE.Pause] = dur - oldDur
        return row


class WorkplaceBuilder(FrameBuilder):


    def __init__(self, placesToWork: dict):

        super(WorkplaceBuilder, self).__init__()
        LOGGER.info("Arbeitsplätze: " + str(placesToWork))
        if len(placesToWork.keys()) == 0:
            raise ValueError("Keine Arbeitsplätze vorhanden")
        self.places_to_work = placesToWork

    def _build_Data(self, df: DataFrame) -> DataFrame:
        df = self._addColumn(df, GOOGLE.Workplace, df[GOOGLE.Name])

        def markWork(x):
            return self.__markWork(x)

        return self._callEachRow(df, markWork)

    def isWorkplace(self, row, workplaces):
        name = row[GOOGLE.Name]
        adress = row[GOOGLE.Address]
        if not isinstance(adress, str) and numpy.isnan(adress):
            adress = None
        isWork = False
        for work in workplaces:
            text: str = str(work)
            if (name and text.find(name) > -1) or \
                    (adress and text.find(adress) > -1):
                isWork = True
                break
        return isWork

    def __markWork(self, row):
        for elem in self.places_to_work:
            workplaces: list = self.places_to_work.get(elem)
            isWorkplace = self.isWorkplace(row, workplaces)
            value = ""
            if isWorkplace:
                value = str(elem)
                LOGGER.info("Der Arbeitsplatz " + elem +
                            " wurde gefunden")
            row[GOOGLE.Workplace] = value
        return row
