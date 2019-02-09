#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import abstractmethod
from datetime import date, datetime, timedelta

import pandas
from Env.TimeConstants import GOOGLE
from Env.Utils import ColumnsWorker, TimesFormatter, logFrame
from config import LOGGER
from pandas.core.frame import DataFrame


class FrameBuilder(object):


    def __init__(self):
        pass

    @abstractmethod
    def _build_Data(self, df) -> DataFrame:
        raise NotImplementedError("FrameBuilder.build ist abstrakt!")

    def _logFrame(self, df, inst=None):
        name = self.__class__
        if inst:
            name = inst
        logFrame(df, name)

    def buildFrame(self, df: DataFrame) -> DataFrame:
        if df.empty:
            LOGGER.warning(
                    "DataFrame ist Leer in Klasse \"%s\"", self.__class__)
        else:
            df = self._build_Data(df)
        return df

    @classmethod
    def _getColumnsInFrame(cls, df: DataFrame, columns: list) -> list:
        return ColumnsWorker.getColumnsInFrame(df, columns)

    @classmethod
    def _reassignColumns(cls, df: DataFrame, columns: list) -> DataFrame:
        return ColumnsWorker.reassignColumns(df, columns)

    @classmethod
    def _addColumn(cls, df: DataFrame, name: str, value=None) -> DataFrame:
        return ColumnsWorker.addColumn(df, name, value)

    @classmethod
    def _addColumns(cls, df: DataFrame, names, value=None) -> DataFrame:
        if isinstance(names, list):
            for name in names:
                df = ColumnsWorker.addColumn(df, name, value)
        else:
            df = ColumnsWorker.addColumns(names, df, value)
        return df

    @classmethod
    def _dropInvertedColumns(cls, df: DataFrame, columns: list) -> DataFrame:
        return ColumnsWorker.removeOtherColumns(columns, df)

    @classmethod
    def _dropColumns(cls, df: DataFrame, columns: list) -> DataFrame:
        return ColumnsWorker.dropColumns(df, columns)

    @classmethod
    def _renameColumns(cls, df: DataFrame, col: dict):
        return ColumnsWorker.renameColumns(df, col)

    @classmethod
    def _callEachRow(cls, df: DataFrame, func) -> DataFrame:
        df = df.apply(func, result_type='expand', axis=1)
        return df


class BuildContainer(FrameBuilder):


    def __init__(self, builders: list):
        super(BuildContainer, self).__init__()
        self.builders = builders

    def _build_Data(self, df: DataFrame) -> DataFrame:
        for item in self.builders:
            try:
                df = item.buildFrame(df)
            except Exception as e:
                LOGGER.error("Fehler beim Bauen der Daten in \
                             Klasse \"%s\":\n%s", item, e)
                self._logFrame(df, self)
                raise
        return df


class IndexBuilder(FrameBuilder):


    def __init__(self, datum: datetime):
        super(IndexBuilder, self).__init__()
        self.build_date = datum

    def _build_Data(self, df: DataFrame) -> DataFrame:
        df = self._addColumn(df, GOOGLE.Index, df[GOOGLE.TimeSpan])
        df = self._addColumn(df, GOOGLE.BuildDate, self.build_date)
        return df


class TimeBuilder(FrameBuilder):


    def __init__(self, dat: datetime, hours_for_tz: int = 2):
        super(TimeBuilder, self).__init__()
        self.build_date = dat
        self.hours_for_tz = hours_for_tz

    def _build_Data(self, df: DataFrame) -> DataFrame:
        series = df[GOOGLE.TimeSpan].apply(pandas.Series)
        times = series.rename(columns={0: GOOGLE.BeginDate, 1: GOOGLE.EndDate})
        df = self._addColumn(df, GOOGLE.BeginDate, times[GOOGLE.BeginDate])
        df = self._addColumn(df, GOOGLE.EndDate, times[GOOGLE.EndDate])

        def convert(row):
            return self.__converttime(row, self.hours_for_tz)

        df = self._callEachRow(df, convert)
        return df

    def __converttime(self, row, hours: int):
        b_time, e_time = self.__getTimeRange(row[GOOGLE.BeginDate],
                                             row[GOOGLE.EndDate],
                                             self.build_date.date(),
                                             hours)
        row[GOOGLE.BeginDate], row[GOOGLE.BeginTime] = b_time.date(), b_time.time()
        row[GOOGLE.EndDate], row[GOOGLE.EndTime] = e_time.date(), e_time.time()
        row[GOOGLE.Duration] = TimesFormatter.calculateDuration(b_time, e_time)
        return row

    def __addTimezone(self, dt: datetime, hoursToAdd: int) -> datetime:
        return dt + timedelta(hours=hoursToAdd)

    def __getTimeRange(self, begin: str, end: str,
                       build: date, hours: int):
        b_time, e_time = TimesFormatter.convertToDatetime(begin=begin,
                                                          end=end)
        b_time = self.__addTimezone(b_time, hours)
        e_time = self.__addTimezone(e_time, hours)
        if e_time > datetime(build.year, build.month, build.day, hour=23,
                             minute=59,
                             second=59):
            e_time = e_time.replace(year=build.year,
                                    month=build.month,
                                    day=build.day,
                                    hour=23,
                                    minute=59,
                                    second=59)
        if b_time < datetime(build.year, build.month, build.day):
            b_time = b_time.replace(year=build.year, month=build.month,
                                    day=build.day, hour=0, minute=0, second=0)
        return b_time, e_time
