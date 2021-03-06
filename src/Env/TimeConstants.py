#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Constants:

    @property
    def Index(self):
        return "TimeIndex"

    @property
    def EndTime(self):
        return "EndTime"

    @property
    def BeginTime(self):
        return "BeginTime"

    @property
    def Duration(self):
        return "Duration"

    @property
    def Pause(self):
        return "Pause"

    @property
    def BuildDate(self):
        return "BuildDate"


class GoogleConstants(Constants):

    @property
    def Address(self):
        return "address"

    @property
    def EndDate(self):
        return "end"

    @property
    def BeginDate(self):
        return "begin"

    @property
    def Category(self):
        return "Category"

    @property
    def Description(self):
        return "description"

    @property
    def Distance(self):
        return "Distance"

    @property
    def Name(self):
        return "name"

    @property
    def Workplace(self):
        return "Workplace"


class BaConstants(Constants):

    @property
    def Pause(self):
        return "Pause (hh:mm)"

    @property
    def Duration(self):
        return "Aufwand in h"

    @property
    def BeginTime(self):
        return "Von"

    @property
    def EndTime(self):
        return "Bis"

    @property
    def BuildDate(self):
        return "Datum"


class IsoConstants(Constants):

    @property
    def Duration(self):
        return "Aufwand"

    @property
    def BeginTime(self):
        return "Von"

    @property
    def EndTime(self):
        return "Bis"

    @property
    def BuildDate(self):
        return "Datum"

    @property
    def Bemerkung(self):
        return "Bemerkung"

    @property
    def BKZ(self):
        return "BKZ"


GOOGLE = GoogleConstants()
ISO = IsoConstants()
BA = BaConstants()
