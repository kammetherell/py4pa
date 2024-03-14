import pandas as pd
import pkg_resources
from subprocess import call
from datetime import datetime

def csv_to_utf8(file):
    """Converts a csv file to utf-8 encoding

    Parameters
    ----------
    file: String
        Path to file to be encoded 

    Returns
    -------
    fName:
        String of path to reformatted file
    """
    df = pd.read_csv(
        file,
        encoding = 'latin'
    )

    fName = file[:-4] + '-reformatted.csv'

    df.to_csv(
        fName,
        index=False
    )

    print(f'{fName} created')

    return fName

def getDateTimeStamp(time=True):
    """Function to generate a Date/Time stamp for the current time

    Parameters
    ----------
    time: Boolean
        Set to True to include time in Date stamp. False returns just date. Defaults to True.

    Returns
    -------
    stamp:
        String of date-time stamp
    """
    now = datetime.now()
    stamp = str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2)
    if time:
        stamp = stamp + "_" + str(now.hour).zfill(2) + str(now.minute).zfill(2)
    return stamp


