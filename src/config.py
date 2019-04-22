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

        self.__check_file_exists(file,success)

        self.__workplaces = self.__get_values("Main", "workplaces")
        dir_path = os.path.dirname(file)
        file = dir_path + "/" + self.config.get("Main", "auth", fallback=None)
        self.__check_file_exists(file, [file])
        with open(file, encoding="utf-8") as f:
            self.__auth = f.read()

    def __check_file_exists(self, file, success:list):
        if not file in success:
            with open(file, "w+", encoding="utf-8"):
                pass
            raise FileNotFoundError(file + " nicht gefunden!")

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
        return ";"

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
