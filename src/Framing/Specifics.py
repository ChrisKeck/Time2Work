#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import abstractmethod

from pandas.core.frame import DataFrame

from Env.TimeConstants import BA, Constants, GOOGLE, ISO
from Env.Utils import ColumnsWorker, TimesFormatter
from Framing.Common import FrameBuilder


class _FrameFinalizer(FrameBuilder):

    def __init__(self, builder: FrameBuilder = None):
        super(_FrameFinalizer, self).__init__()
        self.builder = builder

    def _build_data(self, df: DataFrame) -> DataFrame:
        if self.builder:
            df = self.builder.build_frame(df)
        return self._clean_frame(df)

    @abstractmethod
    def _clean_frame(self, df: DataFrame) -> DataFrame:
        raise NotImplementedError("_FrameFinalizer ist abstrakt!")

    @classmethod
    def _get_temp_name(cls, name) -> str:
        return name + "Temp"


class _ColumnsBuilder(FrameBuilder):

    def __init__(self, instance: Constants):
        super(_ColumnsBuilder, self).__init__()
        self.instance: Constants = instance
        self.otherInstance = GOOGLE

    def _add_constant_columns(self, df: DataFrame, columns) -> DataFrame:
        df = self._add_columns(df, columns)
        return df

    def _rename_existing_columns(self, df: DataFrame,
                                 instance: Constants,
                                 other_instance: Constants) -> DataFrame:
        col = {other_instance.BuildDate: instance.BuildDate,
               other_instance.BeginTime: instance.BeginTime,
               other_instance.EndTime: instance.EndTime,
               other_instance.Duration: instance.Duration,
               other_instance.Pause: instance.Pause}
        df = self._rename_columns(df, col)
        return df

    def _remove_other_columns(self, df: DataFrame, instance) -> DataFrame:
        df = ColumnsWorker.remove_other_columns(instance, df)
        return df

    def _build_data(self, df: DataFrame) -> DataFrame:
        df = self._add_constant_columns(df, self.instance)
        df = self._rename_existing_columns(df, self.instance, self.otherInstance)
        df.reindex()
        df = self._remove_other_columns(df, self.instance)
        return df


class GOOGLEFrameBuilder(_ColumnsBuilder):

    def __init__(self):
        super(GOOGLEFrameBuilder, self).__init__(GOOGLE)


class ISOFrameBuilder(_ColumnsBuilder):

    def __init__(self):
        super(ISOFrameBuilder, self).__init__(ISO)


class BAFrameBuilder(_ColumnsBuilder):

    def __init__(self):
        super(BAFrameBuilder, self).__init__(BA)


class _FormatFinalizer(_FrameFinalizer):

    def __init__(self, instance: Constants):
        super(_FormatFinalizer, self).__init__()
        self.instance = instance

    def __applyformat(self, df, strfunc, name):
        tempname = self._get_temp_name(name)
        df = self._add_column(df, tempname)
        df = df.apply(lambda args: strfunc(args, name, tempname),
                      axis=1, result_type="expand")
        df = self._rename_columns(df, {tempname: name})
        return df

    def _clean_frame(self, df: DataFrame) -> DataFrame:
        df = self.__applyformat(df, self._datetostr, self.instance.BuildDate)
        df = self.__applyformat(df, self._timetostr, self.instance.BeginTime)
        df = self.__applyformat(df, self._timetostr, self.instance.EndTime)
        df = self.__applyformat(df, self._durtostr, self.instance.Duration)
        df = self.__applyformat(df, self._durtostr, self.instance.Pause)
        df.reindex()
        return df

    @abstractmethod
    def _datetostr(self, row, namecol, tempnamecol):
        raise NotImplementedError

    @abstractmethod
    def _timetostr(self, row, namecol, tempnamecol):
        raise NotImplementedError

    @abstractmethod
    def _durtostr(self, row, namecol, tempnamecol):
        raise NotImplementedError


class BAFormatFinalizer(_FormatFinalizer):

    def __init__(self):
        super(BAFormatFinalizer, self).__init__(BA)

    def _datetostr(self, row, namecol, tempnamecol):
        temp = row[namecol]
        row[tempnamecol] = TimesFormatter.to_date_string(temp)
        return row

    def _timetostr(self, row, namecol, tempnamecol):
        temp = row[namecol]
        row[tempnamecol] = TimesFormatter.to_time_string(
            temp, False)
        return row

    def _durtostr(self, row, namecol, tempnamecol):
        temp = row[namecol]
        row[tempnamecol] = TimesFormatter.to_duration_string(temp)
        return row


class ISOFormatFinalizer(_FormatFinalizer):

    def __init__(self):
        super(ISOFormatFinalizer, self).__init__(ISO)

    def _datetostr(self, row, namecol, tempnamecol):
        row[tempnamecol] = TimesFormatter.to_date_string(row[namecol])
        return row

    def _timetostr(self, row, namecol, tempnamecol):
        temp = row[namecol]
        row[tempnamecol] = TimesFormatter.to_time_string(
            temp, False)
        return row

    def _durtostr(self, row, namecol, tempnamecol):
        row[tempnamecol] = TimesFormatter.to_duration_string(row[namecol])
        return row


class _DuplicatesRemoveBuilder(FrameBuilder):

    def __init__(self, instance: object):
        super(_DuplicatesRemoveBuilder, self).__init__()
        self.instance = instance

    def _build_data(self, df: DataFrame) -> DataFrame:
        inst_cols = ColumnsWorker.collect_columns_from_instance(
            self.instance)
        cols = self.__collect_columns_for_unique(
            df, inst_cols, [self.instance.Index])
        return df.drop_duplicates(cols)

    def __collect_columns_for_unique(self, df: DataFrame,
                                     columns: object,
                                     index: object) -> list:
        cols = list()
        for name in df.columns:
            if name in index or name not in columns:
                continue
            cols.append(name)
        return cols


class BADuplicatesRemoveBuilder(_DuplicatesRemoveBuilder):

    def __init__(self):
        super(BADuplicatesRemoveBuilder, self).__init__(BA)


class ISODuplicatesRemoveBuilder(_DuplicatesRemoveBuilder):

    def __init__(self):
        super(ISODuplicatesRemoveBuilder, self).__init__(ISO)
