#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from abc import abstractmethod

from config import LOGGER
from pandas.core.frame import DataFrame


class FrameSaver(object):


    def save(self, df: DataFrame, path: str) -> None:
        path = os.path.normpath(path)
        path = path.replace("[", "").replace("]", "").replace("'", "")
        self._saveFrame(df, path)
        LOGGER.info(
                "Das DataFrame wurde unter dem Pfad \"%s\" erfolgreich gespeichert.", path)

    @abstractmethod
    def _saveFrame(self, df: DataFrame, path: str):
        raise NotImplementedError("FrameSaver ist abstrakt!")


class ExcelFrameSaver(FrameSaver):


    def _saveFrame(self, df: DataFrame, path: str):
        df.to_excel(path)
