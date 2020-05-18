import calendar
from datetime import date, datetime, timezone, timedelta
import os

from scipy.optimize import fsolve

from portfolio_utils import calculate_value
from transactions_utils import TransactionsUtils
from databases.database_access import Database
import databases.database_config as cfg


def set_total_return(year):
    """
    Measure the total return for one year

    :param year: year to measure the total return (1970 - current year)
    :return: N/A
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

        sol = fsolve(equation, 0)
        self.total_return[year] = sol[0] * 100

def get_total_return(year):
    if year not in self.total_return:
        self.set_total_return(year)
    return self.total_return.get(year)


def main():

    report = FinanceUtils()

    finance_db = Database(cfg.my_sql["host"], cfg.my_sql["user"], cfg.my_sql["passwd"], cfg.my_sql["db"])

    file_name = os.path.join(os.environ['HOME'], "Finance", "total_return.txt")

    today_date = datetime.now(tz=timezone(timedelta(hours=-5))).strftime("%Y-%m-%d %H:%M:%S")

    current_year = date.today().year

    try:
        f = open(file_name, "w")
        f.write("Total return \n")
        for year in ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]:
            return_val = round(report.get_total_return(year), 2)

            if len(finance_db.get_table_value("total_returns", "year", "year", year)) == 0:
                # The total return for this year it is not already in the table
                finance_db.insert_values("total_returns", [year, str(return_val)])
            elif year == str(current_year):
                # We can still update the total return for the actual year
                finance_db.update_table_value("total_returns", "return_val", str(return_val), "year", str(current_year))

            print(year + ": " + str(return_val) + " %")
            f.write(year + ": " + str(return_val) + " % \n")
        f.write("Generated at " + str(today_date) + " EST")
        f.close()

        finance_db.close_connection()

    except Exception as err:
        print("Exception error on total_return edition: ", err)


if __name__ == '__main__':
    main()
