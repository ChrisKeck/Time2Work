#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _collections_abc import Iterable

import pandas as pd
from bs4 import BeautifulSoup, ResultSet, BeautifulStoneSoup, Tag
from pandas.core.frame import DataFrame

from Env.TimeConstants import GOOGLE
from config import LOGGER


class FrameCollector:

    def __init__(self):
        self.timeframe = None

    def build(self, text: str) -> DataFrame:
        data: DataFrame = self.__create_frame(text)
        LOGGER.info("Daten wurden ausgelesen:\n" + repr(data))
        return data

    @staticmethod
    def __collect_places(place: ResultSet) -> dict:
        dic = {}
        for elem in place:
            if elem.name != 'Point' and \
                    elem.name != 'description' and \
                    elem.name != 'LineString' and \
                    isinstance(elem, Tag):
                FrameCollector.__collect_place(dic, elem)

        return dic

    @staticmethod
    def __collect_place(dic: dict, elem: Tag):
        if elem.name == 'ExtendedData':
            FrameCollector.__process_extended_data(dic, elem)
        elif elem.name == 'TimeSpan':
            FrameCollector.__process_timespan(dic, elem)

        else:
            FrameCollector.log_tag(elem)
            dic[elem.name] = elem.text
        return dic

    @staticmethod
    def __process_timespan(dic, elem):
        for child in elem.contents:
            if isinstance(child, Tag):
                FrameCollector.log_tag(elem)
                dic[child.name] = child.text

    @staticmethod
    def __process_extended_data(dic, elem):
        for child in elem.contents:
            if isinstance(child, Tag) and \
                    child.attrs['name'] == 'Category':
                text = child.text
                if child.text.strip() == '':
                    text = 'Standing'
                name = child.attrs['name']
                FrameCollector.log_tag(elem)
                dic[name] = text

    @staticmethod
    def log_tag(elem):
        LOGGER.info('Der Tag mit den Namen "' +
                    elem.name + '" und dem Wert "' +
                    elem.text + '" wird hinzugefügt')

    def __process(self, beau_sou: BeautifulSoup) -> Iterable:
        places = []
        index = 0
        for place in beau_sou.find_all('Placemark'):
            found_places = self.__collect_places(place)
            found_places[GOOGLE.Index] = index
            index += 1
            places.append(found_places)
        return places

    def __create_frame(self, text: str) -> DataFrame:
        beau = BeautifulStoneSoup(text)
        places = self.__process(beau)
        data = pd.DataFrame(places)
        return data
