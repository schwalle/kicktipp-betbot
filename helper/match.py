"""
A KickTipp match is simply the representation of a table row in the prediction page.
"""

from datetime import datetime


class Match(object):

    def __init__(self, hometeam: str, roadteam: str, match_date: str, rate_home: str, rate_deuce: str, rate_road: str):
        self.__hometeam = hometeam
        self.__roadteam = roadteam
        self.match_date = match_date
        self.__rate_home = float(rate_home)
        self.__rate_deuce = float(rate_deuce)
        self.__rate_road = float(rate_road)

    def __str__(self):
        return self.__match_date.strftime("%d.%m.%Y %H:%M") \
            + " '" + self.__hometeam \
            + "' vs. '" + self.__roadteam \
            + "' " + " (" + str(self.__rate_home)+";" + str(self.__rate_deuce)+";" + str(self.__rate_road) + ")"

    @property
    def hometeam(self):
        return self.__hometeam

    @hometeam.setter
    def hometeam(self, name):
        self.__hometeam = name

    @property
    def roadteam(self):
        return self.__roadteam

    @roadteam.setter
    def roadteam(self, name):
        self.__roadteam = name

    @property
    def match_date(self):
        return self.__match_date

    @match_date.setter
    def match_date(self, date):
        if type(date) is str:
            try:
                self.__match_date = datetime.strptime(date, '%d.%m.%y %H:%M')
            except Exception:
                self.__match_date = None
        elif type(date) is datetime:
            self.__match_date = date
        else:
            self.__match_date = None

    @property
    def rate_home(self):
        return self.__rate_home

    @property
    def rate_deuce(self):
        return self.__rate_deuce

    @property
    def rate_road(self):
        return self.__rate_road

    @property
    def odds(self):
        return (self.__rate_home, self.__rate_deuce, self.__rate_road)
