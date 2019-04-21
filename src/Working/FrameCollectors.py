#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _collections_abc import Iterable

import pandas as pd
from bs4 import BeautifulSoup, ResultSet, BeautifulStoneSoup, Tag
from pandas.core.frame import DataFrame

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
            if elem.name != 'Point' and elem.name != 'description' and elem.name != 'LineString' and isinstance(elem, (Tag)):
                LOGGER.info('Der Tag mit den Namen "' + elem.name + '" hat den Wert "' + elem.text + '"')
                FrameCollector.__collect_place(dic, elem)

        return dic

    @staticmethod
    def __collect_place(dic: dict, elem: Tag):
        if elem.name=='ExtendedData':
            for child in elem.contents:
                if isinstance(child,Tag) and child.attrs['name'] == 'Category':
                    text=child.text
                    if child.text.strip()=='':
                        text='Standing'
                    dic[child.attrs['name']]=text
        elif elem.name=='TimeSpan':
            for child in elem.contents:
                if isinstance(child, Tag):
                    dic[child.name] = child.text
        else:
            dic[elem.name]=elem.text
        return dic

    def __process(self, beau_sou: BeautifulSoup) -> Iterable:
        places = []
        for place in beau_sou.find_all('Placemark'):
            found_places = self.__collect_places(place)
            places.append(found_places)
        return places

    def __create_frame(self, text: str) -> DataFrame:
        beau = BeautifulStoneSoup(text)
        places = self.__process(beau)
        LOGGER.info(places)
        data = pd.DataFrame(places)
        return data
