#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import abstractmethod
from datetime import date, datetime, timedelta

from pandas.core.frame import DataFrame

from Env.TimeConstants import GOOGLE
from Env.Utils import ColumnsWorker, TimesFormatter, log_frame
from config import LOGGER


class FrameBuilder(object):

    def __init__(self):
        pass

    @abstractmethod
    def _build_data(self, df) -> DataFrame:
        raise NotImplementedError("FrameBuilder.build ist abstrakt!")

    def _log_frame(self, df, inst=None):
        name = self.__class__
        if inst:
            name = inst
        log_frame(df, name)

    def build_frame(self, df: DataFrame) -> DataFrame:
        if df.empty:
            LOGGER.warning(
                "DataFrame ist Leer in Klasse \"%s\"", self.__class__)
        else:
            df = self._build_data(df)
        if df.empty:
            LOGGER.warning(
                "DataFrame ist Leer in Klasse \"%s\"", self.__class__)
        return df

    @classmethod
    def _get_columns_in_frame(cls, df: DataFrame, columns: list) -> list:
        return ColumnsWorker.get_columns_in_frame(df, columns)

    @classmethod
    def _reassign_columns(cls, df: DataFrame, columns: list) -> DataFrame:
        return ColumnsWorker.reassign_columns(df, columns)

    @classmethod
    def _add_column(cls, df: DataFrame, name: str, value=None) -> DataFrame:
        return ColumnsWorker.add_column(df, name, value)

    @classmethod
    def _add_columns(cls, df: DataFrame, names, value=None) -> DataFrame:
        if isinstance(names, list):
            for name in names:
                df = ColumnsWorker.add_column(df, name, value)
        else:
            df = ColumnsWorker.add_columns(names, df, value)
        return df

    @classmethod
    def _drop_inverted_columns(cls, df: DataFrame, columns: list) -> DataFrame:
        return ColumnsWorker.remove_other_columns(columns, df)

    @classmethod
    def _drop_columns(cls, df: DataFrame, columns: list) -> DataFrame:
        return ColumnsWorker.drop_columns(df, columns)

    @classmethod
    def _rename_columns(cls, df: DataFrame, col: dict):
        return ColumnsWorker.rename_columns(df, col)

    @classmethod
    def _call_each_row(cls, df: DataFrame, func) -> DataFrame:
        df = df.apply(func, result_type='expand', axis=1)
        return df


class BuildContainer(FrameBuilder):

    def __init__(self, builders: list):
        super(BuildContainer, self).__init__()
        self.builders = builders

    def _build_data(self, df: DataFrame) -> DataFrame:
        for item in self.builders:
            try:
                df = item.build_frame(df)
            except Exception as e:
                LOGGER.error("Fehler beim Bauen der Daten in \
                             Klasse \"%s\":\n%s", item, e)
                self._log_frame(df, self)
                raise
        return df


class IndexBuilder(FrameBuilder):

    def __init__(self, datum: datetime):
        super(IndexBuilder, self).__init__()
        self.build_date = datum

    def _build_data(self, df: DataFrame) -> DataFrame:
        df = self._add_column(df, GOOGLE.Index, df[GOOGLE.Description])
        df = self._add_column(df, GOOGLE.BuildDate, self.build_date)
        return df


class TimeBuilder(FrameBuilder):

    def __init__(self, dat: datetime, hours_for_tz: int = 2):
        super(TimeBuilder, self).__init__()
        self.build_date = dat
        self.hours_for_tz = hours_for_tz

    def _build_data(self, df: DataFrame) -> DataFrame:

        def convert(row):
            return self.__convert_time(row, self.hours_for_tz)

        df = self._call_each_row(df, convert)
        return df

    def __convert_time(self, row, hours: int):
        b_time, e_time = self.__getTimeRange(row[GOOGLE.BeginDate],
                                             row[GOOGLE.EndDate],
                                             self.build_date.date(),
                                             hours)
        row[GOOGLE.BeginDate], row[GOOGLE.BeginTime] = b_time.date(), b_time.time()
        row[GOOGLE.EndDate], row[GOOGLE.EndTime] = e_time.date(), e_time.time()
        row[GOOGLE.Duration] = TimesFormatter.calculate_duration(b_time, e_time)
        return row

    def __add_timezone(self, dt: datetime, hours_to_add: int) -> datetime:
        return dt + timedelta(hours=hours_to_add)

    def __getTimeRange(self, begin: str, end: str,
                       build: date, hours: int):
        b_time, e_time = TimesFormatter.convert_to_datetime(begin=begin,
                                                            end=end)
        b_time = self.__add_timezone(b_time, hours)
        e_time = self.__add_timezone(e_time, hours)
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
