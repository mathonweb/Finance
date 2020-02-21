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
import os
from datetime import date, datetime
from logging import exception

from portfolio_utils import PortfolioUtils
from scipy.optimize import fsolve
from transactions_utils import TransactionsUtils
# scientific computing package
import pandas as pd


class FinanceUtils:
    def __init__(self):
        self.total_return = {}

    def set_total_return(self, year):
        # print("Enter set_total_return")
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
                    move_expr += (row['Quantity'] * row['Price']) / \
                                 ((1 + x) ** (nb_days_from_investing.days / (365 + (1*calendar.isleap(date_year)))))

                # Equation from https://www.disnat.com/forms/mrcc2/comprendre-vos-rendements-fr.pdf
                return begin_year + move_expr - end_period / (1+x)

            sol = fsolve(equation, 0)
            self.total_return[year] = sol[0] * 100

    def calculate_value(self, calendar_date):
        portfolio_on_date = PortfolioUtils(calendar_date).get_portfolio()

        value = 0
        for index, row in portfolio_on_date.iterrows():
            if row["Quantity"] > 0:
                value += row["Price"] * row["Quantity"]

        return value

    def get_total_return(self, year):
        if year not in self.total_return:
            self.set_total_return(year)
        return self.total_return.get(year)


def main():

    report = FinanceUtils()

    file_name = os.path.join(os.environ['HOME'], "Finance", "total_return.txt")

    try:
        f = open(file_name, "w")
        print("Total return")
        for year in ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]:
            print(year + ": " + str(round(report.get_total_return(year), 2)) + " %")
            f.write(year + ": " + str(round(report.get_total_return(year), 2)) + " % \n")
        print("Generated at " + str(datetime.now()))
        f.close()

    except Exception as err:
        print("Exception error on total_return edition: ", err)


if __name__ == '__main__':
    main()
