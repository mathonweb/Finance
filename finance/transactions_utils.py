import sys
from datetime import date
import configparser

import pandas as pd

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
        config = configparser.ConfigParser()
        config.read_file(open('config.ini'))

        self._ticker = ticker
        self._file = get_file(config['DEFAULT']['transactions_file'])
        self._transactions_df = self._set_transactions()

    def _set_transactions(self):
        """
        Create a dataframe with all transactions related to a ticker or for all tickers

        :return: Dataframe with transactions
        """

        file_df = pd.read_csv(self._file, index_col=None)

        if self._ticker != "all":
            transactions_df = file_df.loc[file_df['Ticker'] == self._ticker]
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
        return self._ticker

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
            return self._transactions_df
        else:
            return self._transactions_df[self._transactions_df["Date"] <= market_date]

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

        return self._transactions_df[(begin_date <= self._transactions_df["Date"]) &
                                    (self._transactions_df["Date"] <= end_date)]

    def get_transactions_number(self):
        """
        Return number of transactions related to the ticker(s)

        :return: Number of transactions for the ticker(s)
        """
        return len(self._transactions_df)

    def get_first_date_transaction(self):
        return self._transactions_df["Date"][0]
