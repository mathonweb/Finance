import calendar
from datetime import date, datetime
import os

from scipy import optimize
import numpy as np
from pytz import timezone
import pandas as pd

import config
from portfolio_utils import calculate_value
from transactions_utils import TransactionsUtils
from config import annual_returns_file
from utils.errors_finder import find_errors_in_logs
from utils.s3_client import send_file
from utils.logger import logger


class Finance:
    def __init__(self):
        self.total_annual_return = pd.DataFrame(columns={"Year", "Total return %"})

    def _calculate_total_return(self, year):
        """
        Measure the total return for one year

        :param year: year to measure the total return (1970 - current year)
        :return: Year total return (%)
        """

        if year > date.today().year or year < 1970:
            raise Exception('Year to measure total return must be included in 1970 - current year, you set: ' + year)
        else:
            # VMD - Value at the beginning
            begin_year = calculate_value(date(year, 1, 1))
            transactions_util = TransactionsUtils("all")

            if year == date.today().year:
                # YTD calculation
                # VMF - Value at the end
                end_period = calculate_value(date.today())
                transactions = transactions_util.get_transactions_period(date(year, 1, 1), date.today())
            else:
                # Complete year calculation
                # VMF - Value at the end
                end_period = calculate_value(date(year, 12, 31))
                transactions = transactions_util.get_transactions_period(date(year, 1, 1), date(year, 12, 31))

            # Get the transactions for the period and build the expression
            def equation(f):
                x = f
                move_expr = 0
                for index, row in transactions.iterrows():
                    nb_days_from_investing = row['Date'] - date(year, 1, 1)
                    move_expr += (row['Quantity'] * row['Price']) / \
                                 ((1 + x) ** (nb_days_from_investing.days / (365 + (1*calendar.isleap(year)))))

                # Equation from https://www.disnat.com/forms/mrcc2/comprendre-vos-rendements-fr.pdf
                return begin_year + move_expr - end_period / (1+x)

            sol = optimize.fsolve(equation, x0=np.array([0]))
            return sol[0] * 100

    def create_total_annual_return(self):
        transactions_util = TransactionsUtils("all")
        first_date_transaction = transactions_util.get_first_date_transaction()
        first_year_transaction = first_date_transaction.year

        for year in range(first_year_transaction, date.today().year + 1):
            annual_return = {"Year": str(year), "Total return %": round(self._calculate_total_return(year), 2)}
            self.total_annual_return = self.total_annual_return.append(annual_return, ignore_index=True)

    def get_total_annual_return(self):
        return self.total_annual_return


def create_total_return_report(return_values):
    """
    Create the list with total return every year

    :param return_values: List of total return values
    :return: N/A
    """

    file_name = os.path.join(annual_returns_file)

    today_date = datetime.now(timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")

    try:
        f = open(file_name, "w")

        f.write("Performance \n")
        f.write("Total return \n")

        for annual_return in return_values.itertuples(index=False):
            f.write(annual_return.year + ": " + str(annual_return.annual_return) + " %")
            f.write("\n")

        f.write("Generated at " + str(today_date) + " EST" + "\n")

        if find_errors_in_logs(config.logs_file):
            f.write("Errors happened, see logs file ")

        f.close()

        send_file(file_name)

    except OSError as err:
        logger.error("Exception error on total_return file creation: ", err)


def main():
    """
    Call function to calculate the Total Return for every year and create a report

    :return: N/A
    """
    finance = Finance()
    finance.create_total_annual_return()
    total_return_df = finance.get_total_annual_return()
    total_return_df.to_csv("annual_total_return.csv", index=False, index_label=False)
    send_file("annual_total_return.csv")


if __name__ == '__main__':
    main()
