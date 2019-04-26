#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from numpy import datetime64
from pandas.core.frame import DataFrame
from pandas.core.groupby import DataFrameGroupBy

from Env.TimeConstants import GOOGLE
from Framing.Common import FrameBuilder


class _GroupBuilder(FrameBuilder):

    def _build_data(self, df: DataFrame) -> DataFrame:
        df = self._initFrame(df)
        grp = self._createGroup(df)
        agggrp = self.__aggregateGroup(grp)
        grpdf = DataFrame(agggrp)
        return grpdf

    def _initFrame(self,
                   df: DataFrame) -> DataFrame:
        return df

    def __aggregateGroup(self,
                         group: DataFrameGroupBy):
        group = group.apply(self._applyToGroup)
        return group

    @abstractmethod
    def _applyToGroup(self, group: DataFrameGroupBy):
        raise NotImplementedError()

    @abstractmethod
    def _createGroup(self, df: DataFrame) -> DataFrameGroupBy:
        raise NotImplementedError()


class DurationGroupBuilder(_GroupBuilder, ABC):

    def __init__(self, workplaces: list):
        super(DurationGroupBuilder, self).__init__()
        self.workplaces = workplaces

    def __filterValues(self, df, datum: datetime64):
        data = DataFrame()
        for it in self.workplaces:
            dfTogrp = df[df[GOOGLE.Workplace] == it]
            dfTogrp = dfTogrp[(dfTogrp[GOOGLE.BuildDate] >= datum) &
                              (dfTogrp[GOOGLE.BuildDate] <= datum)]
            if not dfTogrp.empty:
                dfTogrp = self._add_column(dfTogrp, GOOGLE.Workplace, it)
                dfTogrp = self._add_column(dfTogrp, GOOGLE.BuildDate, datum)
                data = data.append(dfTogrp)
        return data

    def _build_data(self, df: DataFrame) -> DataFrame:
        selectedDates = list()
        newDf = DataFrame()
        for item in df[GOOGLE.BuildDate].get_values():
            if item not in selectedDates:
                selectedDates.append(item)
        for datum in selectedDates:

            filtereddf = self.__filterValues(df, datum)
            for wp in self.workplaces:
                wpdf:DataFrame=filtereddf.where(filtereddf[GOOGLE.Workplace]==wp)
                wpdf=wpdf.dropna(axis=0,how='all')
                if wpdf.empty:
                    continue
                wpdf = self.aggrateDuration(wpdf)
                newDf = newDf.append(wpdf.drop_duplicates())
        return newDf

    def aggrateDuration(self, filtereddf):
        sumDur =filtereddf[GOOGLE.Duration].agg({sum})['sum']
        begintime = filtereddf[GOOGLE.BeginTime].agg({min})['min']
        endtime = filtereddf[GOOGLE.EndTime].agg({max})['max']
        filtereddf = self._drop_columns(filtereddf, [GOOGLE.Duration,
                                                     GOOGLE.BeginTime,
                                                     GOOGLE.EndTime])
        filtereddf = self._add_column(filtereddf,
                                      GOOGLE.Duration,
                                      sumDur)
        filtereddf = self._add_column(filtereddf,
                                      GOOGLE.BeginTime,
                                      begintime)
        filtereddf = self._add_column(filtereddf,
                                      GOOGLE.EndTime,
                                      endtime)
        return filtereddf
