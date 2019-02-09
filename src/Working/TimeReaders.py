#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import time
from abc import abstractmethod
from datetime import datetime
from os import environ

import requests
from Env.Utils import TimesFormatter
from config import LOGGER
from urllib3.exceptions import RequestError


class TimeReader:


    def __init__(self, cookies: str):
        self.cookies = cookies

    @abstractmethod
    def _readTime(self, date: datetime) -> str:
        raise NotImplementedError

    def readText(self, date: datetime) -> str:
        result = self._readTime(date)

        LOGGER.debug("Daten wurden geladen:\n" + result)
        return result

    def _createUrl(self, date: datetime) -> str:
        urltime = "{2}!2i{1}!3i{0}!2m3!1i{2}!2i{1}!3i{0}".format(
                date.day, date.month - 1, date.year)
        url = "https://www.google.de/maps/timeline/kml?authuser=0&pb=!1m8!1m3!1i" + urltime
        LOGGER.debug("Download-Link wurd ermittelt:\n" + url)
        return url


class WebrequestReader(TimeReader):


    def __init___(self, cookies: str):
        super(WebrequestReader, self, ).__init__(cookies)

    def _readTime(self, date: datetime) -> str:
        """
        Get KML file from your location history and save it in a chosen folder
        """
        time.sleep(5)
        url = self._createUrl(date)
        cookies = dict(cookie=self.cookies)
        res = requests.get(url, cookies=cookies)
        result = res.text
        if res.status_code != 200:
            raise RequestError("", url,
                               "Fehlercode: " +
                               str(res.status_code) +
                               "\n" +
                               result.text)

        return result


class Cmd2FileReader(TimeReader):


    def __createKml(self, date: datetime) -> str:
        url = self._createUrl(date)
        command = self.cookies.replace("$(URL)", url)
        return command.replace("$(OUTPUT)", self.__getTempPath(date))

    def __getTempPath(self, date: datetime) -> str:
        path = os.path.join(
                environ['TEMP'], "{0}.{1}.{2}_Maps.kml".format(date.year, date.month, date.day))
        return path

    def _readTime(self, date: datetime) -> str:

        pa = self.__getTempPath(date)
        if not os.path.exists(pa):
            kmlurl = self.__createKml(date)
            time.sleep(5)
            process = subprocess.Popen(kmlurl, shell=True, encoding="utf-8")
            # Launch the shell command:
            process.communicate()

        if not os.path.exists(pa):
            raise FileNotFoundError(pa)
        with open(pa, 'r', encoding='utf-8') as f:
            output = f.read()
        return output


class TimelineReader:


    def __init__(self, reader: TimeReader):
        self.reader = reader

    def readTime(self, date_von: datetime, date_bis: datetime) -> dict:
        date_text = dict()
        days = TimesFormatter.getRangeBetweenDays(date_von, date_bis)
        for current in days:
            current = TimesFormatter.convertTimezone(current)
            now = TimesFormatter.convertTimezone(datetime.now())
            if current < now:
                text = self.reader.readText(current)
                date_text.update({current: text})
        return date_text
