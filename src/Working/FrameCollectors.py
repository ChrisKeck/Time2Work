#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _collections_abc import Iterable

import pandas as pd
from bs4 import BeautifulSoup, NavigableString, ResultSet, BeautifulStoneSoup, Tag
from config import LOGGER
from pandas.core.frame import DataFrame


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
            LOGGER.info(elem)
            if elem.name != 'Point':
                if isinstance(elem, (Tag)):
                    FrameCollector.__collect_place(dic, elem)

        return dic

    @staticmethod
    def __collect_place(dic: dict, elem: Tag):
        child = list(elem.children)
        datas = elem.find_all('Data')

        if len(child) == 1:
            dic.update({elem.name.title(): ''.join(child)})
        elif len(datas) > 1:
            for data in datas:
                dic.update({data.attrs['name']: data.text})
        else:
            LOGGER.warn(child)
            dic.update({elem.name: [d.text for d in child]})

        return dic

    def __process(self, beau_sou: BeautifulSoup) -> Iterable:
        places = []
        for place in beau_sou.find_all('Placemark'):
            found_places = self.__collect_places(place)
            places.append(found_places)
        return places

    def __create_frame(self, text: str) -> DataFrame:
        beau = BeautifulStoneSoup(text.replace("\n", "").replace(" ", ""))
        places = self.__process(beau)
        LOGGER.info(places)
        data = pd.DataFrame(places)
        return data
