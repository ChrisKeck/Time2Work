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
        df = self._init_frame(df)
        grp = self._create_group(df)
        agggrp = self.__aggregate_group(grp)
        grpdf = DataFrame(agggrp)
        return grpdf

    def _init_frame(self,
                    df: DataFrame) -> DataFrame:
        return df

    def __aggregate_group(self,
                          group: DataFrameGroupBy):
        group = group.apply(self._apply_to_group)
        return group

    @abstractmethod
    def _apply_to_group(self, group: DataFrameGroupBy):
        raise NotImplementedError()

    @abstractmethod
    def _create_group(self, df: DataFrame) -> DataFrameGroupBy:
        raise NotImplementedError()


class DurationGroupBuilder(_GroupBuilder, ABC):

    def __init__(self, workplaces: list):
        super(DurationGroupBuilder, self).__init__()
        self.workplaces = workplaces

    def __filter_values(self, df, datum: datetime64):
        data = DataFrame()
        for it in self.workplaces:
            df_togrp = df[df[GOOGLE.Workplace] == it]
            df_togrp = df_togrp[(df_togrp[GOOGLE.BuildDate] >= datum) &
                                (df_togrp[GOOGLE.BuildDate] <= datum)]
            if not df_togrp.empty:
                df_togrp = self._add_column(df_togrp, GOOGLE.Workplace, it)
                df_togrp = self._add_column(df_togrp, GOOGLE.BuildDate, datum)
                data = data.append(df_togrp)
        return data

    def _build_data(self, df: DataFrame) -> DataFrame:
        new_df = DataFrame()
        selected_dates = self.__collect_build_dates(df)
        for datum in selected_dates:

            filtered: DataFrame = self.__filter_values(df, datum)
            if filtered.empty:
                continue
            aggregated_df = self.__aggregate_df(filtered)
            new_df = new_df.append(aggregated_df)
        return new_df

    def __aggregate_df(self, filtered_df):
        for wp in self.workplaces:
            wpdf: DataFrame = filtered_df.where(filtered_df[GOOGLE.Workplace] == wp)
            wpdf = wpdf.dropna(axis=0, how='all')
            if wpdf.empty:
                continue
        return self.__aggrate_duration(wpdf)

    def __collect_build_dates(self, df: DataFrame) -> list:
        selected_dates = list()
        for item in df[GOOGLE.BuildDate].get_values():
            if item not in selected_dates:
                selected_dates.append(item)
        return selected_dates

    def __aggrate_duration(self, filtered_df) -> DataFrame:
        sum_dur = filtered_df[GOOGLE.Duration].agg({sum})['sum']
        begintime = filtered_df[GOOGLE.BeginTime].agg({min})['min']
        endtime = filtered_df[GOOGLE.EndTime].agg({max})['max']
        filtered_df = self._drop_columns(filtered_df, [GOOGLE.Duration,
                                                       GOOGLE.BeginTime,
                                                       GOOGLE.EndTime])
        filtered_df = self._add_column(filtered_df,
                                       GOOGLE.Duration,
                                       sum_dur)
        filtered_df = self._add_column(filtered_df,
                                       GOOGLE.BeginTime,
                                       begintime)
        filtered_df = self._add_column(filtered_df,
                                       GOOGLE.EndTime,
                                       endtime)
        return filtered_df.drop_duplicates()
