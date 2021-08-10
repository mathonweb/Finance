import calendar
from datetime import date, datetime
import os

from scipy import optimize
import numpy as np
from pytz import timezone

import config
from portfolio_utils import calculate_value
from transactions_utils import TransactionsUtils
from config import annual_returns_file
from utils.errors_finder import find_errors_in_logs
from utils.s3_client import send_file
from utils.logger import logger


def calculate_total_return(year):
    """
    Measure the total return for one year

    :param year: year to measure the total return (1970 - current year)
    :return: Year total return (%)
    """
    date_year = int(year)

    if date_year > date.today().year or date_year < 1970:
        raise Exception('Year to measure total return must be included in 1970 - current year, you set: ' + year)
    else:
        # VMD - Value at the beginning
        begin_year = calculate_value(date(date_year, 1, 1))
        transactions_util = TransactionsUtils("all")

        if date_year == date.today().year:
            # YTD calculation
            # VMF - Value at the end
            end_period = calculate_value(date.today())
            transactions = transactions_util.get_transactions_period(date(date_year, 1, 1), date.today())
        else:
            # Complete year calculation
            # VMF - Value at the end
            end_period = calculate_value(date(date_year, 12, 31))
            transactions = transactions_util.get_transactions_period(date(date_year, 1, 1), date(date_year, 12, 31))

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

        sol = optimize.fsolve(equation, x0=np.array([0]))
        return sol[0] * 100


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

        for year in return_values:
            f.write(str(year) + ": " + str(return_values[year]) + " %")
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
    return_val = dict()

    transactions_util = TransactionsUtils("all")
    first_date_transaction = transactions_util.get_first_date_transaction()
    first_year_transaction = first_date_transaction.year

    for year in range(first_year_transaction, date.today().year+1):
        return_val[year] = round(calculate_total_return(str(year)), 2)
        print(str(year) + ": " + str(return_val[year]) + " %")

    create_total_return_report(return_val)


if __name__ == '__main__':
    main()
