#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
from datetime import datetime

from Framing.Common import BuildContainer
from Framing.Specifics import (BADuplicatesRemoveBuilder, BAFormatFinalizer, BAFrameBuilder, ISODuplicatesRemoveBuilder, ISOFormatFinalizer,
                               ISOFrameBuilder)
from Mocks import NoBuildingTransformerMock, PublisherMock, TransformerTimePoiMock
from config import Config
from pandas.core.frame import DataFrame


class TransformerTest(unittest.TestCase):


    def setUp(self):
        self.workplaces = Config("./resources/Time2Work.ini")
        with open("./resources/history-2018-07-20.kml", "r", encoding="utf-8") as f:
            url = f.read()
        self.url = url
        self.id = self.workplaces.timestamp + self.workplaces.id

    def tearDown(self):
        pass

    def createFinalizers(self):
        ba = BuildContainer([BAFrameBuilder(),
                             BAFormatFinalizer(),
                             BADuplicatesRemoveBuilder()])
        iso = BuildContainer([ISOFrameBuilder(),
                              ISOFormatFinalizer(),
                              ISODuplicatesRemoveBuilder()])
        pathClean = {
            "C:/Temp/ba_" + self.id + ".xlsx": ba,
            "C:/Temp/iso_" + self.id + ".xlsx": iso,
            "C:/Temp/ori_" + self.id + ".xlsx": BuildContainer([])}
        return pathClean

    def createTransformer(self):
        transformer = TransformerTimePoiMock(self.url, self.workplaces.places)

        return transformer

    def test_WennTransformiertWurde_DannExistierenDieEntsprechendenDateien(self):
        transformer = self.createTransformer()
        transformer.transform(datetime(2018, 7, 20), datetime(
                2018, 7, 20), self.createFinalizers())
        assert os.path.exists("C:/Temp/ba_" + self.id + ".xlsx")
        assert os.path.exists("C:/Temp/iso_" + self.id + ".xlsx")

    def testWennOhneAenderungenDerDatenTransformiertWurde_DannExistierenDieEntsprechendeDatei(self):
        pathClean = {
            "C:/Temp/nobuilders_" + self.id + ".xlsx": BuildContainer([])}
        transformer = NoBuildingTransformerMock(
                self.url, self.workplaces.places)
        transformer.transform(datetime(2018, 7, 20), datetime(
                2018, 7, 20), pathClean)
        assert os.path.exists("C:/Temp/nobuilders_" + self.id + ".xlsx")
        assert os.path.getsize("C:/Temp/nobuilders_" +
                               self.id + ".xlsx") > 1

    def testName3(self):
        pub = PublisherMock(os.path.realpath("./resources/LN.xlsx"))
        pub.integrate(DataFrame())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
