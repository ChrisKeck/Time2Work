#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os

from Framing.Common import BuildContainer
from Working.Transformers import CommandToExcelTransformer
from config import Config


class Time2Work:


    def __init__(self, config: Config, basedir: str):
        self.config = config
        self.basedir = basedir

    def createSpecificBuilders(self, fins):
        finList = list()
        for fin in fins:
            splitted = fin.split(".")
            clsname = splitted[-1]
            splitted.remove(clsname)
            module = ".".join(splitted)
            import importlib
            module = importlib.import_module(module)
            class_ = getattr(module, clsname)
            instance = class_()
            finList.append(instance)
        return finList

    def createOutputFilePath(self, config: Config, basedir, item):
        filename = "{0}_{1}.{2}".format(config.fileprefix[item],
                                        config.id,
                                        config.fileExtension)
        path = os.path.join(basedir, filename)
        return path

    def createWorkDict(self, config, basedir):
        work_dict = dict()
        for item in config.sectionPlaces:
            fins = config.finalizer[item]
            finList = self.createSpecificBuilders(fins)
            path = self.createOutputFilePath(config, basedir, item)
            work_dict.update({path: BuildContainer(finList)})

        return work_dict

    def start(self, von: datetime.datetime, bis: datetime.datetime):
        config: Config = self.config
        basedir = self.basedir
        work_dict = self.createWorkDict(config, basedir)

        transformer = CommandToExcelTransformer(config.auth, config.places)
        transformer.transform(von, bis, work_dict)
