#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod
from datetime import datetime
from os import path

import pandas
from Env.Utils import logFrame
from Framing.Common import (BuildContainer, FrameBuilder, IndexBuilder, TimeBuilder)
from Framing.Custom import PauseDurationBuilder, WorkplaceBuilder
from Framing.Grouping import DurationGroupBuilder
from Framing.Specifics import GOOGLEFrameBuilder
from Working.FrameCollectors import FrameCollector
from Working.FrameSavers import ExcelFrameSaver
from Working.TimeReaders import Cmd2FileReader, TimeReader, TimelineReader
from config import LOGGER
from pandas.core.frame import DataFrame


class Transformer(object):


    def __create_framebuilder(self) -> FrameCollector:
        framebuilder = FrameCollector()
        return framebuilder

    def __buildSingleFrame(self, elem, text):
        LOGGER.info("Building Frame For " + str(elem) + "...")
        framebuilder: FrameCollector = self.__create_framebuilder()
        other = framebuilder.build(text)
        builder = self._createBuilder(elem)
        other = builder.buildFrame(other)
        LOGGER.info("Frame built For " + repr(elem) + "\n" + repr(other))
        return other

    def __tranform_to_frame(self,
                            date_von: datetime,
                            date_bis: datetime) -> DataFrame:
        time_reader = self._create_timereader()
        text_date_dict: dict = time_reader.readTime(date_von, date_bis)
        df = DataFrame()
        for elem in text_date_dict:
            other = self.__buildSingleFrame(elem, text_date_dict[elem])
            if other.empty:
                logFrame(df,
                         self,
                         "Es wird das bis jetzt produzierte DataFrame angezeigt,\
                         weil der neue Teil \"%s\" bei der Verarbeitung leer geworden \
                         ist!".format(elem))
            else:
                df = df.append(other)
        return df

    def __clean(self, df, item):
        cleaned = df.copy(deep=True)
        cleaned = item.buildFrame(cleaned)
        return cleaned

    def transform(self, date_von: datetime,
                  date_bis: datetime, custom_work_paths: dict) -> None:
        df: DataFrame = self.__tranform_to_frame(date_von, date_bis)
        self.__finalizeFrame(df, custom_work_paths)

    def __finalizeFrame(self, df: DataFrame, custom_work_paths: dict) -> None:
        for item in custom_work_paths:
            cleaned = self.__clean(df, custom_work_paths[item])
            if cleaned.empty:
                errorpath = path.join(path.dirname(str(item)),
                                      "error_" + path.basename(item))
                logFrame(df, item, "Das ursprüngliche DataFrame wird wegen keinen Daten \
                                    unter dem Pfad %s gespeichert.".format(errorpath))
                self._saveFrame(df, errorpath)
            else:
                self._saveFrame(cleaned, str(item))

    @abstractmethod
    def _createBuilder(self, dat: datetime) -> FrameBuilder:
        raise NotImplementedError("_Builder.build ist abstrakt!")

    def _create_timereader(self) -> TimelineReader:
        core_reader = self._create_reader()
        reader = TimelineReader(core_reader)
        return reader

    @abstractmethod
    def _create_reader(self) -> TimeReader:
        raise NotImplementedError("_create_reader ist abstrakt!")

    @abstractmethod
    def _saveFrame(self, df: DataFrame, path: str) -> None:
        raise NotImplementedError("_saveFrame ist abstrakt!")


class CommandToExcelTransformer(Transformer):


    def __init__(self, content: str, workplaces: dict):
        super(CommandToExcelTransformer, self).__init__()
        self.content = content
        self.workplaces = workplaces

    def _createBuilder(self, dat: datetime) -> FrameBuilder:
        wp = self.workplaces
        return BuildContainer([GOOGLEFrameBuilder(),
                               IndexBuilder(dat),
                               TimeBuilder(dat),
                               WorkplaceBuilder(wp),
                               DurationGroupBuilder(list(wp.keys().__iter__())),
                               PauseDurationBuilder()])

    def _saveFrame(self, df: DataFrame, path: str) -> None:
        frsa = ExcelFrameSaver()
        frsa.save(df, path)

    def _create_reader(self) -> TimeReader:
        core_reader = Cmd2FileReader(self.content)
        return core_reader


class FramePublisher:


    def __init__(self, framepath):
        self.df = pandas.read_excel(framepath)

    def integrate(self, other: DataFrame):
        df: DataFrame = self.df

        # self._logFrame(df, self)
        self._logFrame(repr(df.to_dict()), self)

    def _logFrame(self, df, inst=None):
        name = inst
        with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
            LOGGER.warning("##########\nGesamtes Frame in Klasse \"%s\":\n%s\n#############",
                           str(name),
                           df)
