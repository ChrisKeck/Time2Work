#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
from datetime import datetime

from pandas.core.frame import DataFrame

from Framing.Common import BuildContainer
from Framing.Specifics import (BADuplicatesRemoveBuilder, BAFormatFinalizer, BAFrameBuilder, ISODuplicatesRemoveBuilder,
                               ISOFormatFinalizer,
                               ISOFrameBuilder, )
from Mocks import NoBuildingTransformerMock, PublisherMock, TransformerTimePoiMock
from config import Config

root = os.path.expanduser("~/PycharmProjects/Time2Work")
class TransformerTest(unittest.TestCase):


    def setUp(self):
        self.workplaces = Config(root + "/resources/Time2Work.ini")
        with open(root + "/resources/history-2018-01-01.kml", "r", encoding="utf-8") as f:
            url = f.read()
        self.url = url
        self.wid = self.workplaces.timestamp + self.workplaces.id

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
            root + "/target/ba_" + self.wid + ".xlsx": ba,
            root + "/target/iso_" + self.wid + ".xlsx": iso,
            root + "/target/ori_" + self.wid + ".xlsx": BuildContainer([])}
        return pathClean

    def createTransformer(self, url):
        transformer = TransformerTimePoiMock(url, self.workplaces.places)
        return transformer

    def test_WennTransformiertWurde_DannExistierenDieEntsprechendenDateien(self):
        transformer = self.createTransformer(self.url)
        transformer.transform(datetime(2018, 1, 1), datetime(
                2018, 1, 1), self.createFinalizers())
        assert os.path.exists(root+ "/target/ba_" + self.wid + ".xlsx")
        assert os.path.exists(root+ "/target/iso_" + self.wid + ".xlsx")


    def testWennOhneAenderungenDerDatenTransformiertWurde_DannExistierenDieEntsprechendeDatei(self):
        pathClean = {
            root + "/target/nobuilders_" + self.wid + ".xlsx": BuildContainer([])}
        transformer = NoBuildingTransformerMock(
                self.url, self.workplaces.places)
        transformer.transform(datetime(2018, 7, 20), datetime(
                2018, 7, 20), pathClean)
        assert os.path.exists(root + "/target/nobuilders_" + self.wid + ".xlsx")
        assert os.path.getsize(root + "/target/nobuilders_" +
                               self.wid + ".xlsx") > 1

    def testName3(self):
        pub = PublisherMock(root + "/resources/LN.xlsx")
        pub.integrate(DataFrame())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
