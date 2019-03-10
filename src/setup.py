#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
        # Application name:
        name="Time2Work",

        # Version number (initial):
        version="0.8.0",

        # Application author details:
        author="Keck Christian",
        author_email="keckchris@outlook.com",

        # Packages
        packages=["src"],

        # Include additional files into the package
        include_package_data=True,

        # Details
        url="http://pypi.python.org/pypi/Time2Work_v080/",

        #
        license="LICENSE",
        description="Leistungsnachweise individuell erstellen lassen anhand von deinem Bewegungsmuster",

        long_description=open("../README.txt").read(),

        # Dependent packages (distributions)
        install_requires=[
            "flask", "pandas", "Arrow", "dateutil", 'numpy', 'beautifulsoup4', 'requests', 'urllib3'
            ],
        )
