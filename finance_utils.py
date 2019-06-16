# -------------------------------------------------------------------------------
# Name:         finance_utils
# Purpose:      Contains financial functions
#
# Author:       Mathieu Guilbault
#
# Created:      2019-02-07
# Copyright:    (c) Mathieu Guilbault 2019
# -------------------------------------------------------------------------------

from datetime import date
from share_utils import ShareUtils
from transactions_utils import TransactionsUtils
import os
# scientific computing package
import pandas as pd
from historical_utils import HistoricalUtils


class FinanceUtils:
    def __init__(self):
        pass

    #def isnan(num):
    #    return num != num
    #
    #
    #def getfloordate(df, date):
    #    # return the floor date closest to the selected date
    #    date2find = date
    #    i = datetime.timedelta(0)
    #    while date2find.strftime("%y%m%d") not in df.index:
    #        i = i - datetime.timedelta(1)
    #        date2find = date + i
    #    print(date2find)
    #    return date2find
    #
    #
    #def getceildate(df, date):
    #    # return the floor date closest to the selected date
    #    date2find = date
    #    i = datetime.timedelta(0)
    #    while date2find.strftime("%y%m%d") not in df.index:
    #        i = i + datetime.timedelta(1)
    #        date2find = date + i
    #    print(date2find)
    #    return date2find
    #
    #
    #def getannualreturn(df, year):
    #
    #    # return the first date of the year 1
    #    date1 = getfloordate(df, datetime.date(year1, 1, 1))
    #
    #    # return the last date of the year 2
    #    date2 = getceildate(df, datetime.date(year2, 12, 31))
    #
    #    # do the calculation if year2 is after year1
    #    if date2 < date1:
    #        print("error: you must enter and ending year later than the first year")
    #        raise exception('dateerror')
    #
    #    # compound annual growth rate
    #    # cagr = (ending value / beginning value) ^ (1 / # of years) - 1
    #    cagr = df.loc[date2.strftime("%y%m%d"), 'adj close'] / df.loc[date1.strftime("%y%m%d"), 'adj close'] - 1
    #
    #    return cagr


def main():
    #file = 'historical_data/vus.to.csv'
    #df = pd.read_csv(file, index_col='date', parse_dates=True, na_values='nan')

    #year1 = 2014
    #year2 = 2014
    #
    ## todo validate year available in the excel files
    #
    #try:
    #    cagr = getannualreturn(df, year1, year2)
    #    # todo comprendre pourquoi je n'arrive pas au rendement annuel de vanguard et yahoo (12.65% pour 2014)
    #    print('{:2.2f}%' .format(cagr*100))
    #except exception:
    #    print('error with dates')

    try:
        file = str(os.environ['transactions_path']) + "\\" + "transactions.csv"
    except Exception as e:
        print(e)

    # create an instance of transactions utils
    transactions_list = TransactionsUtils(file).get_transactions()

    my_date = date(2019, 1, 1)

    # create an instance of historical utils
    historical_list = HistoricalUtils("XEF.TO", [2012, 1, 1], [2019, 1, 1])

    share_xef = ShareUtils(transactions_list, historical_list.historical_df, "XEF.TO", my_date)
    print("Number of shares = " + str(share_xef.get_share_nb()))
    print("Mean cost = " + str(share_xef.get_mean_cost()))
    print("Actual price = " + str(share_xef.actual_price))


if __name__ == '__main__':
    main()
