#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _collections_abc import Iterable
from datetime import date, datetime, time

import pandas
from arrow.arrow import Arrow
from dateutil.relativedelta import relativedelta
from numpy import ndarray
from pandas.core.frame import DataFrame
from pandas.core.series import Series

from src.config import LOGGER


class ColumnsWorker(object):


    @staticmethod
    def getColumnsInFrame(df: DataFrame, columns: list) -> list:
        dropped_columns = list()
        for item in columns:
            if item in df.columns:
                dropped_columns.append(item)
            else:
                LOGGER.debug(str(item) + " wurde nicht gefunden!")

        return dropped_columns

    @staticmethod
    def reassignColumns(df: DataFrame, columns: list) -> DataFrame:
        columns = ColumnsWorker.getColumnsInFrame(df, columns)
        return df[columns]

    @staticmethod
    def __fillList(total_rows, tempvalues) -> list:
        values = list()
        if len(tempvalues) == 1 and total_rows > 1:
            for dummy in range(0, total_rows):
                values.append(tempvalues[0])
        else:
            values = tempvalues
        return values

    @staticmethod
    def addColumn(df: DataFrame, name: str, value=None) -> DataFrame:
        values = list()
        total_rows = len(df.axes[0])
        if isinstance(value, Series):
            tempvalues = value.get_values()
            values = ColumnsWorker.__fillList(total_rows, tempvalues)
        elif isinstance(value, ndarray):
            values = ColumnsWorker.__fillList(total_rows, value)
        elif isinstance(value, Iterable) and not isinstance(value, str):
            values = ColumnsWorker.__fillList(total_rows, list(value))
        else:
            for dummy in range(0, total_rows):
                values.append(value)
        df[name] = values
        return df

    @staticmethod
    def dropColumns(df: DataFrame, columns: list) -> DataFrame:
        dropped_columns = ColumnsWorker.getColumnsInFrame(df, columns)
        return df.drop(dropped_columns, axis=1)

    @staticmethod
    def renameColumns(df: DataFrame, col: dict):
        torename = dict()
        for item in col:
            if item == col[item]:
                continue
            torename.update({item: col[item]})
        df = ColumnsWorker.dropColumns(df, list(torename.values().__iter__()))
        df = df.rename(torename,
                       axis=1)

        return df

    @staticmethod
    def collectColumnsFromInstance(instance):
        names = dir(instance)
        values = list()
        for name in names:
            if not name.startswith("_"):
                try:
                    func = getattr(instance, name)
                    values.append(func)
                except Exception as e:
                    LOGGER.error(
                            "{0} ist nicht abrufbar!\nException: {1}", name, e)
                    raise
        return values

    @staticmethod
    def removeColumns(instance, df: DataFrame):
        values = ColumnsWorker.collectColumnsFromInstance(instance)
        return df.drop(values, axis=1)

    @staticmethod
    def removeOtherColumns(instance, df: DataFrame):
        values = ColumnsWorker.collectColumnsFromInstance(instance)
        torems = list()
        for item in df.columns:
            if item not in values:
                torems.append(item)
        return df.drop(torems, axis=1)

    @staticmethod
    def addColumns(instance, df: DataFrame, default=None):
        values = ColumnsWorker.collectColumnsFromInstance(instance)
        for item in values:
            if item in df:
                continue
            df = ColumnsWorker.addColumn(df, item, default)
        return df


class TimesFormatter:


    @staticmethod
    def convertTimezone(dtime) -> datetime:
        """
        Convert datetimes from UTC to localtime zone
        """
        if isinstance(dtime, datetime):
            utc_datetime = dtime
        elif dtime:
            utc_datetime = datetime.strptime(
                str(dtime), "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            raise ValueError("dtime ist null!")
        return utc_datetime.replace(tzinfo=None)

    @staticmethod
    def roundTime(dt: datetime, shiftOp="+") -> datetime:
        ardt: Arrow = Arrow.fromdatetime(dt)
        minute = 0
        if 0 < dt.minute <= 15:
            minute = 15 - dt.minute
        elif 15 < dt.minute <= 30:
            minute = 30 - dt.minute
        elif 30 < dt.minute <= 45:
            minute = 45 - dt.minute
        elif dt.minute > 45:
            minute = 60 - dt.minute
        if shiftOp != "+":
            ardt = ardt.shift(minutes=-15)
        ardt = ardt.shift(minutes=minute)
        return ardt.datetime.replace(second=0, microsecond=0, tzinfo=None)

    @staticmethod
    def calculateDuration(b_time, e_time) -> int:
        if isinstance(b_time, time) or isinstance(e_time, time):
            b_time = datetime(1, 1, 1, b_time.hour, b_time.minute)
            e_time = datetime(1, 1, 1, e_time.hour, e_time.minute)
        delta = relativedelta(e_time, b_time)
        hours = (delta.days * 24) + delta.hours
        minutes = delta.minutes + (hours * 60)
        duration = int(minutes)
        return duration

    @staticmethod
    def toDurationString(dur: int) -> str:
        if  dur<0:
            dur=dur*(-1)
        hours, minutes = divmod(int(dur), 60)
        durdate=None
        try:
            durdate = datetime(1, 1, 1, hours, minutes)
        except  ValueError as ex:
            pass
        durdate = TimesFormatter.roundTime(durdate)
        return "{:02d}:{:02d}".format(durdate.hour, durdate.minute)

    @staticmethod
    def toTimeString(ti: time, isProcent=False) -> str:
        if isProcent:
            res = TimesFormatter.toTimeInProcentString(ti)
        else:
            res = "{:%H:%M}".format(datetime(1, 1, 1, ti.hour, ti.minute))
        return res

    @staticmethod
    def toTimeInProcentString(ti: time) -> str:
        procent: float = 0
        durdate = datetime(1, 1, 1, ti.hour, ti.minute)
        if durdate.minute == 15:
            procent = 0.25
        elif durdate.minute == 30:
            procent = 0.5
        elif durdate.minute == 45:
            procent = 0.75
        timeprocent = float(durdate.hour) + procent
        return "{:.2f}".format(timeprocent)

    @staticmethod
    def toDateString(da: date, formatstr="%d.%m.%Y") -> str:
        temp = datetime(da.year, da.month, da.day)
        return temp.strftime(formatstr)

    @staticmethod
    def __calcMinutesFromString(b_time) -> int:
        bsplitted = str(b_time).split(":")
        bhours = int(bsplitted[0]) * 60
        minutes = bhours + int(bsplitted[1])
        return minutes

    @staticmethod
    def calculateMinutes(b_time: str) -> int:
        bmins = TimesFormatter.__calcMinutesFromString(b_time)
        return bmins

    @staticmethod
    def getRangeBetweenDays(b_time: datetime, e_time: datetime) -> Iterable:
        days = list()
        b_time = datetime(b_time.year, b_time.month, b_time.day)
        e_time = datetime(e_time.year, e_time.month, e_time.day)
        for elem in Arrow.range("day", b_time, e_time):
            days.append(elem.datetime)
        return days

    @staticmethod
    def convertToDatetime(begin: str, end: str):
        begin = TimesFormatter.convertTimezone(begin)
        end = TimesFormatter.convertTimezone(end)
        begin = TimesFormatter.roundTime(
            begin, "+")
        end = TimesFormatter.roundTime(end, "+")
        return begin, end


def logFrame(df, inst=None, msg=""):
    name = "#UNKNOWN#"
    if inst:
        name = inst
    if msg and len(msg) > 0:
        msg = "--------------\n" + msg + "\n---------------------\n"
    with pandas.option_context('display.max_rows', 5,
                               'display.max_columns', None):
        LOGGER.warning("##########\n%sGesamtes Frame in Klasse \"%s\":\n%s\n#############",
                       msg,
                       str(name),
                       df)
