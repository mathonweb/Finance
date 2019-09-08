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
from portfolio_utils import PortfolioUtils
# scientific computing package
import pandas as pd


class FinanceUtils:
    def __init__(self):
        pass

    def set_annual_return(self, year):
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

    today_portfolio = PortfolioUtils(date.today())
    print("Today Portfolio")
    print(today_portfolio.get_portfolio())
    begin_year_portfolio = PortfolioUtils(date(2019, 1, 1))
    print("Begining of the year Portfolio")
    print(begin_year_portfolio.get_portfolio())


if __name__ == '__main__':
    main()
