
#from __future__ import division
import re
#import codecs
import datetime
from collections import defaultdict

def return_datetime(date,time = False,minute = False,setting = "eu"):
    """Put a date and time string in the python datetime format."""
    if setting == "eu":            
        parse_date = re.compile(r"(\d{2})-(\d{2})-(\d{4})")
        pds = parse_date.search(date).groups()
        date = [pds[2],pds[1],pds[0]]
    elif setting == "vs":
        parse_date = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
        date = parse_date.search(date).groups(1)
    elif setting == "twitter":
        month = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, 
            "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
        parse_dt = re.compile(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d+) " +
            r"(\d{2}:\d{2}:\d{2}) \+\d+ (\d{4})")
        dtsearch = parse_dt.search(date).groups()
        date = [dtsearch[3],month[dtsearch[0]],dtsearch[1]]
        time = dtsearch[2]
    if time:
        parse_time = re.compile(r"^(\d{2}):(\d{2})")
        timeparse = parse_time.search(time).groups(1)
        if minute:
            datetime_obj = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(timeparse[0]),0,0)
        else:
            datetime_obj = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(timeparse[0]),int(timeparse[1]),0)
    else:
        datetime_obj = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),0,0,0)
    return datetime_obj

def timerel(time1,time2,unit):
    """Return the difference in time in a given time unit between two datetime objects.""" 
    if unit == "day":
        day = (time1.date() - time2.date()).days
        if day < 0:
            day = day*-1
        return day
    else:
        dif = time1 - time2
        if unit == "hour":
            hours = (int(dif.days) * 24) + (int(dif.seconds) / 3600)
            return hours
        if unit == "minute":   
            minutes = (int(dif.days) * 1440) + int(dif.seconds / 60)
            return minutes
