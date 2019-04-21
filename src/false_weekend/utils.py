# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/FalseWeekend
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Version: 0.0.1 


# Copied and modified from ReMemorize


from aqt import mw
import datetime



def parseDate(days):
    try:
        return getDays(days)
    except ValueError: #non date format
        return days
    # except TypeError: #passed date
        # showInfo("Already passed due date")
        # return None


def getDays(date_str):
    d=datetime.datetime.today()
    today=datetime.datetime(d.year, d.month, d.day)
    try:
        due=datetime.datetime.strptime(date_str,'%m/%d/%Y')
    except ValueError:
        date_str=date_str+'/'+str(d.year)
        due=datetime.datetime.strptime(date_str,'%m/%d/%Y')
    diff=(due-today).days
    # if diff<1: raise TypeError
    return diff #can be negative

