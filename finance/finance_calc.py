import calendar
from datetime import date
import configparser

from scipy import optimize
import numpy as np
import pandas as pd

from finance.portfolio_utils import calculate_value
from finance.transactions_utils import TransactionsUtils
from finance.utils.s3_client import send_file


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


def main():
    """
    Call function to calculate the Total Return for every year and create a report

    :return: N/A
    """
    config = configparser.ConfigParser()
    config.read_file(open('config.ini'))

    finance = Finance()
    finance.create_total_annual_return()
    total_return_df = finance.get_total_annual_return()
    total_return_df.to_csv(config['DEFAULT']['annual_returns_file'], index=False, index_label=False)
    send_file(config['DEFAULT']['annual_returns_file'])


if __name__ == '__main__':
    main()
