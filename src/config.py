#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from _collections_abc import Iterable
from configparser import ConfigParser
from datetime import datetime

from flask import logging


class Config(object):

    def __init__(self, file: str):
        """
        Constructor
        """
        if file is None:
            return
        self.config: ConfigParser = ConfigParser()
        success = self.config.read(file, encoding="utf-8")
        dir = os.path.dirname(file)
        if file not in success:
            raise FileNotFoundError(file + " nicht gefunden!")
        self.__workplaces = self.__get_values("Main", "workplaces")
        file = dir + "/" + self.config.get("Main", "auth", fallback=None)
        if not file:
            raise FileNotFoundError(file + " nicht gefunden!")
        with open(file, encoding="utf-8") as f:
            self.__auth = f.read()

    def __get_values(self, key, option) -> list:
        return self.config.get(key, option, fallback="").split(self.delimiter)

    def __get_dict(self, option: str) -> dict:
        result = dict()
        for item in self.__workplaces:
            values = self.__get_values(item, option)
            if len(values) > 0:
                result.update({item: values})
        return result

    @property
    def timestamp(self):
        return datetime.utcnow().strftime('%Y%m%d_%H_%M_%S.%f')[:-3]

    @property
    def places(self) -> dict:
        return self.__get_dict("places")

    @property
    def file_extension(self):
        return "xlsx"

    @property
    def delimiter(self) -> str:
        return "|"

    @property
    def section_places(self) -> Iterable:
        return self.__workplaces

    @property
    def fileprefix(self) -> dict:
        return self.__get_dict("fileprefix")

    @property
    def finalizer(self) -> dict:
        return self.__get_dict("finalizer")

    @property
    def id(self) -> str:
        return str(os.getpid())

    @property
    def auth(self) -> str:
        return self.__auth


__handler = logging.logging.getLogger()
LOGGER = logging.create_logger(__handler)

DEBUG = True

THREADS_PER_PAGE = 4

CSRF_ENABLED = True
CSRF_SESSION_KEY = "secret"
