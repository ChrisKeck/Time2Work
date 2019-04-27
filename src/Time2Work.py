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

    def create_specific_builders(self, fins):
        fin_list = list()
        for fin in fins:
            if not fin:
                continue
            splitted = fin.split(".")
            clsname = splitted[-1]
            splitted.remove(clsname)
            module = ".".join(splitted)
            import importlib
            module = importlib.import_module(module)
            class_ = getattr(module, clsname)
            instance = class_()
            fin_list.append(instance)
        return fin_list

    def create_output_file_path(self, config: Config, basedir, item):
        filename = "{0}_{1}.{2}".format(config.fileprefix[item],
                                        config.id,
                                        config.file_extension)
        path = os.path.join(basedir, filename)
        return path

    def create_work_dict(self, config, basedir):
        work_dict = dict()
        for item in config.section_places:
            fins = config.finalizer[item]
            fin_list = self.create_specific_builders(fins)
            path = self.create_output_file_path(config, basedir, item)
            work_dict.update({path: BuildContainer(fin_list)})

        return work_dict

    def start(self, von: datetime.datetime, bis: datetime.datetime):
        config: Config = self.config
        basedir = self.basedir
        work_dict = self.create_work_dict(config, basedir)

        transformer = CommandToExcelTransformer(config.auth, config.places)
        transformer.transform(von, bis, work_dict)
