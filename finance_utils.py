# -------------------------------------------------------------------------------
# Name:         finance_utils
# Purpose:      Contains financial functions
#
# Author:       Mathieu Guilbault
#
# Created:      2019-02-07
# Copyright:    (c) Mathieu Guilbault 2019
# -------------------------------------------------------------------------------
import calendar
from datetime import date, datetime
from logging import exception

from portfolio_utils import PortfolioUtils
from scipy.optimize import fsolve
from transactions_utils import TransactionsUtils
# scientific computing package
import pandas as pd


class FinanceUtils:
    def __init__(self):
        self.annual_returns = {}

    def set_annual_return(self, year):
        # print("Enter set_annual_return")
        date_year = int(year)
        if date_year > date.today().year:
            raise exception('dateerror')
        else:
            # VMD - Value at the beginning
            begin_year = self.calculate_value(date(date_year, 1, 1))
            transactions_util = TransactionsUtils("all")

            if date_year == date.today().year:
                # YTD calculation
                # VMF - Value at the end
                end_period = self.calculate_value(date.today())
                transactions = transactions_util.get_transactions_period(date(date_year, 1, 1), date.today())
            else:
                # Complete year calculation
                # VMF - Value at the end
                end_period = self.calculate_value(date(date_year, 12, 31))
                transactions = transactions_util.get_transactions_period(date(date_year, 1, 1), date(date_year, 12, 31))

            # x = symbols('x')
            # Get the transactions for the period and build the expression
            def equation(f):
                x = f
                move_expr = 0
                for index, row in transactions.iterrows():
                    nb_days_from_investing = row['Date'] - date(date_year, 1, 1)
                    move_expr += (row['Quantity'] * row['Price']) / ((1 + x) ** (nb_days_from_investing.days / (365 + (1*calendar.isleap(date_year)))))

                # Equation from https://www.disnat.com/forms/mrcc2/comprendre-vos-rendements-fr.pdf
                return begin_year + move_expr - end_period / (1+x)

            sol = fsolve(equation, 0)
            self.annual_returns[year] = sol[0] * 100

    def calculate_value(self, calendar_date):
        portfolio_on_date = PortfolioUtils(calendar_date).get_portfolio()

        value = 0
        for index, row in portfolio_on_date.iterrows():
            if row["Quantity"] > 0:
                value += row["Price"] * row["Quantity"]

        return value

    def get_annual_return(self, year):
        if year not in self.annual_returns:
            self.set_annual_return(year)
        return self.annual_returns.get(year)


def main():

    report = FinanceUtils()

    f = open("annual_returns.txt", "w")

    for year in ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]:
        print("Annual return " + year + ": " + str(round(report.get_annual_return(year), 2)) + " %")
        f.write("Annual return " + year + ": " + str(round(report.get_annual_return(year), 2)) + " % \n")

    f.close


if __name__ == '__main__':
    main()
