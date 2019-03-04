#-------------------------------------------------------------------------------
# Name:         finance_utils
# Purpose:      Contains financial functions
#
# Author:       Mathieu Guilbault
#
# Created:      2019-02-07
# Copyright:    (c) Mathieu Guilbault 2019
#-------------------------------------------------------------------------------

from datetime import datetime
# Scientific computing package
import pandas as pd


def isNaN(num):
    return num != num


def getFloorDate(df, date):
    # Return the floor date closest to the selected date
    date2find = date
    i = datetime.timedelta(0)
    while date2find.strftime("%Y%m%d") not in df.index:
        i = i - datetime.timedelta(1)
        date2find = date + i
    print(date2find)
    return date2find


def getCeilDate(df, date):
    # Return the floor date closest to the selected date
    date2find = date
    i = datetime.timedelta(0)
    while date2find.strftime("%Y%m%d") not in df.index:
        i = i + datetime.timedelta(1)
        date2find = date + i
    print(date2find)
    return date2find


def getAnnualReturn(df, year1, year2):

    # Return the first date of the year 1
    date1 = getFloorDate(df, datetime.date(year1, 1, 1))

    # Return the last date of the year 2
    date2 = getCeilDate(df, datetime.date(year2, 12, 31))

    # Do the calculation if year2 is after year1
    if date2 < date1:
        print("Error: You must enter and ending year later than the first year")
        raise Exception('dateError')

    # Compound Annual Growth Rate
    # CAGR = (Ending Value / Beginning Value) ^ (1 / # of years) - 1
    cagr = df.loc[date2.strftime("%Y%m%d"), 'Adj Close'] / df.loc[date1.strftime("%Y%m%d"), 'Adj Close'] - 1

    return cagr


def main():
    file = 'Historical_data/VUS.TO.csv'
    df = pd.read_csv(file, index_col='Date', parse_dates=True, na_values='nan')

    year1 = 2014
    year2 = 2014

    # TODO Validate year available in the Excel files

    try:
        cagr = getAnnualReturn(df, year1, year2)
        # TODO Comprendre pourquoi je n'arrive pas au rendement annuel de Vanguard et Yahoo (12.65% pour 2014)
        print('{:2.2f}%' .format(cagr*100))
    except Exception:
        print('Error with dates')


if __name__ == '__main__':
    main()
