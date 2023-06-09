import re
from dateutil import parser
from datefinder import find_dates

from datetime import datetime
import os
from nltk import word_tokenize


def dateFormat(stringList):
    string = ""
    for word in stringList:
        string += word+" "
    date_content = find_dates(string, True, True)

    for match in date_content:
        s=str(match[0])
        if("00:00:00" in s):
            s=s.replace("00:00:00","")
        string = string.replace(str(match[1]), s)

    # dated = word_tokenize(string)
    # return dated
    return string



