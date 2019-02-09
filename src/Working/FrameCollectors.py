#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _collections_abc import Iterable

import pandas as pd
from bs4 import BeautifulSoup
from config import LOGGER
from pandas.core.frame import DataFrame


class FrameCollector:


    def __init__(self):
        self.timeframe = None

    def build(self, text: str) -> DataFrame:
        data: DataFrame = self.__createFrame(text)
        LOGGER.info("Daten wurden ausgelesen:\n" + repr(data.head(2)))
        return data

    def __collectPlaces(self, place):
        dic = {}
        for elem in place:
            if elem.name != 'Point':
                child = list(elem.children)
                datas = elem.find_all('Data')
                if len(child) == 1:
                    dic.update({elem.name.title(): ''.join(child)})
                elif len(datas) > 1:
                    for data in datas:
                        dic.update({data.attrs['name']: data.text})

                else:
                    dic.update({elem.name: [d.text for d in child]})

        return dic

    def __process(self, beau_sou: BeautifulSoup) -> Iterable:
        places = []
        for place in beau_sou.find_all('Placemark'):
            found_places = self.__collectPlaces(place)
            places.append(found_places)
        return places

    def __createFrame(self, text: str) -> DataFrame:
        beau = BeautifulSoup(text, 'xml')
        places = self.__process(beau)
        data = pd.DataFrame(places)
        return data
