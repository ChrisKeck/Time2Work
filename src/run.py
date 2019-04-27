#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime
from getopt import GetoptError, getopt

from Time2Work import Time2Work
from config import Config


def help_output():
    print("Noch nicht verfübar")
    sys.exit()


def create_config(setting_file):
    try:
        return Config(setting_file)
    except FileNotFoundError:

        raise


def main(argv):
    setting_file = "../resources/Time2Work.ini"
    output = os.curdir
    von = None
    bis = None
    debug = False
    try:
        opts, args = getopt(argv,
                            "hc:do:f:t:",
                            ["help", "config=",
                             "debug", "output=",
                             "from=", "till="])
        print("Options: {0}\nArgs: {1}".format(opts, args))
    except GetoptError:
        help_output()
        raise
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
        elif opt in ("-d", "--debug"):
            debug = True
        elif opt in ("-c", "--config"):
            setting_file = arg
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-f", "--from"):
            von = convert_date(arg)
        elif opt in ("-t", "--till"):
            bis = convert_date(arg)
    Config.DEBUG = debug
    config = create_config(setting_file)
    worker = Time2Work(config, output)
    worker.start(von, bis)


def convert_date(arg):
    try:
        res = datetime.strptime(arg, "%d.%m.%Y")
        return res
    except:
        print("Datum in folgenden Format angeben: \"%d.%m.%Y\"\nz.B.: 1.1.2000")
        raise


if __name__ == '__main__':
    main(sys.argv[1:])
