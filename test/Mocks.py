#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import datetime

from pandas.core.frame import DataFrame

from Framing.Common import (BuildContainer, FrameBuilder, IndexBuilder, TimeBuilder)
from Framing.Custom import (PauseDurationBuilder, WorkplaceBuilder)
from Framing.Grouping import DurationGroupBuilder
from Framing.Specifics import GOOGLEFrameBuilder
from Working.TimeReaders import TimeReader
from Working.Transformers import CommandToExcelTransformer, FramePublisher

root = os.path.expanduser("~/PycharmProjects/Time2Work")
filedate = "2018-01-01"
fromnow = datetime(2018, 1, 1)
tonow = datetime(2018, 1, 1)


class BaseReaderMock(TimeReader):

    def _readTime(self, dummy: datetime) -> str:
        return self.cookies


class TransformerMock(CommandToExcelTransformer):

    def __init__(self, content: str, workplaces: dict):
        super(TransformerMock, self).__init__(content, workplaces)
        self.content = content

    def _create_reader(self) -> TimeReader:
        return BaseReaderMock(self.content)


class NoBuildingTransformerMock(TransformerMock):

    def __init__(self, content: str, workplaces: dict):
        super(NoBuildingTransformerMock, self).__init__(content, workplaces)
        self.content = content

    def _create_reader(self) -> TimeReader:
        return BaseReaderMock(self.content)

    def _create_builder(self, dummy: datetime) -> FrameBuilder:
        return BuildContainer([])


class TransformerTimePoiMock(TransformerMock):

    def _create_builder(self, dat: datetime) -> FrameBuilder:
        return BuildContainer([GOOGLEFrameBuilder(),
                               IndexBuilder(dat),
                               TimeBuilder(dat),
                               WorkplaceBuilder(self.workplaces),
                               DurationGroupBuilder(self.workplaces.keys()),
                               PauseDurationBuilder()])


class PublisherMock(FramePublisher):

    def integrate(self, other: DataFrame):
        FramePublisher.integrate(self, other)
