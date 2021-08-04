import sys
from datetime import date

import pandas as pd

from config import transactions_file
from utils.s3_client import get_file
from utils.logger import logger


def validate_transactions(transactions_df):
    """
    Verify if the values in the transactions file are valid

    :param transactions_df: csv file with transactions, follow the format
    :return: True = Validation successful, False = Otherwise
    """
    for index, row in transactions_df.iterrows():
        if not (row["Date"] <= date.today() and
                row['Price'] > 0 and
                row['Quantity'] != 0):
            return False

    return True


class TransactionsUtils:
    """
    Contain transactions info for a ticker or all tickers in the transactions file
    """

    def __init__(self, ticker):
        """
        TransactionsUtils Constructor

        :param ticker: Ticker name (Ex: XIC.TO), all = for all tickers
        """
        self.ticker = ticker
        self.file = get_file(transactions_file)
        self.transactions_df = self._set_transactions()

    def _set_transactions(self):
        """
        Create a dataframe with all transactions related to a ticker or for all tickers

        :return: Dataframe with transactions
        """

        file_df = pd.read_csv(self.file, index_col=None)

        if self.ticker != "all":
            transactions_df = file_df.loc[file_df['Ticker'] == self.ticker]
        else:
            transactions_df = file_df

        transactions_df["Date"] = pd.to_datetime(transactions_df["Date"]).dt.date

        validation_result = validate_transactions(transactions_df)
        if not validation_result:
            logger.error("Please, fix your transaction info")
            sys.exit("Error, see log file")

        return transactions_df

    def get_ticker(self):
        """
        Get the ticker associated to this instance

        :return: Ticker name
        """
        return self.ticker

    def get_transactions(self, market_date):
        """
        Get all transactions up to this date

        :param market_date: Highest limit date to get the transactions
        :return: Dataframe with transactions
        """
        if not isinstance(market_date, date):
            logger.error("market_date must be a Date type")
            return None

        if market_date is None:
            return self.transactions_df
        else:
            return self.transactions_df[self.transactions_df["Date"] <= market_date]

    def get_transactions_period(self, begin_date, end_date):
        """
        Get all transactions between these two dates

        :param begin_date: Lowest limit date to get the transactions
        :param end_date: Highest limit date to get the transactions
        :return: Dataframe with transactions
        """
        if not isinstance(begin_date, date):
            logger.error("You must set a Date format for begin_date: " + begin_date)
            return None

        if not isinstance(end_date, date):
            logger.error("You must set a Date format for end_date: " + end_date)
            return None

        return self.transactions_df[(begin_date <= self.transactions_df["Date"]) &
                                    (self.transactions_df["Date"] <= end_date)]

    def get_transactions_number(self):
        """
        Return number of transactions related to the ticker(s)

        :return: Number of transactions for the ticker(s)
        """
        return len(self.transactions_df)


def main():
    # Create an instance of Transactions Utils
    transactions_list = TransactionsUtils("all")
    print("Number of transactions = " + str(transactions_list.get_transactions_number()))

    transactions = transactions_list.get_transactions(date.today())
    print("Transactions = ")
    print(str(transactions))

    period = transactions_list.get_transactions_period(date(2014, 1, 1), date(2014, 12, 31))
    print("Transactions in 2014 = ")
    print(str(period))


if __name__ == '__main__':
    main()
