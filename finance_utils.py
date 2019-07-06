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
    def __init__(self, transactions_file):
        self.transactions = TransactionsUtils(transactions_file)

    def setAnnualReturn(self, year):
        pass

    # def getannualreturn(df, year):
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
    try:
        file = str(os.environ['INVESTING_PATH']) + "\\" + "transactions.csv"
    except Exception as e:
        print(e)

    # create an instance of transactions utils
    transactions_list = TransactionsUtils(file).get_transactions()

    my_date = date.today()

    share_xef = ShareUtils(transactions_list, "XEF.TO", my_date)
    print("Number of shares = " + str(share_xef.set_share_nb()))
    print("Mean cost = " + str(share_xef.set_mean_cost()))
    print("Actual price = " + str(share_xef.actual_price))


if __name__ == '__main__':
    main()
