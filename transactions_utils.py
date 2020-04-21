from datetime import date
import os
import pandas as pd

from config import transaction_file_path


class TransactionsUtils:
    """
    Contain transaction info for a ticker or all ticker in the transactions file
    """
    def __init__(self, ticker, transactions_file):
        """
        TransactionsUtils Constructor

        :param ticker: Thicker name (Ex: XIC.TO), all: for all tickers
        :param transactions_file: Absolute path to the transactions.csv file
        """
        self.ticker = ticker
        self.file = self.validate_transaction_file(transactions_file)
        self.transactions_df = self.set_transactions()

    def get_tickers(self):
        """
        Get the ticker associated to this instance

        :return: Ticker name
        """
        return self.ticker

    def set_transactions(self):
        """
        Create a dataframe with all transactions related to a ticker or for all tickers

        :return: Dataframe with transactions
        """

        # Create a pandas dataframe
        #    Ticker   Date        Price   Quantity    Commission
        # 0  XEF.TO   01/01/2017  10.9    5         9.99

        file_df = pd.read_csv(self.file)

        if self.ticker is not "all":
            transactions_df = file_df.loc[file_df['Ticker'] == self.ticker]
        else:
            transactions_df = file_df

        transactions_df = self.format_dates(transactions_df)
        self.validate_transactions(transactions_df)
        self.sort_transactions(transactions_df)

        return transactions_df

    def get_transactions(self, market_date):
        """
        Get all transactions up to this date

        :param market_date: Highest limit date to get the transactions
        :return: Dataframe with transactions
        """
        if not isinstance(market_date, date):
            raise Exception("You must set a Date format for market_date: " + market_date)

        if market_date is None:
            return self.transactions_df
        else:
            return self.transactions_df[self.transactions_df['Date'] <= market_date]

    def get_transactions_period(self, begin_date, end_date):
        """
        Get all transactions between these two dates

        :param begin_date: Lowest limit date to get the transactions
        :param end_date: Highest limit date to get the transactions
        :return: Dataframe with transactions
        """
        if not isinstance(begin_date, date):
            raise Exception("You must set a Date format for begin_date: " + begin_date)

        if not isinstance(end_date, date):
            raise Exception("You must set a Date format for end_date: " + end_date)

        return self.transactions_df[(begin_date <= self.transactions_df['Date']) &
                                    (self.transactions_df['Date'] <= end_date)]

    @staticmethod
    def validate_transaction_file(transactions_file):
        """
        Validate the csv file existing path

        :param transactions_file: csv file with transactions, follow the format
        :return: csv file absolute path if exists, exit otherwise
        """
        if os.path.exists(transactions_file):
            return transactions_file
        else:
            raise Exception("Transaction file is not valid: " + str(transactions_file))

    @staticmethod
    def format_dates(transactions_df):
        """
        Convert Excel date format into Date format

        :param transactions_df: csv file with transactions, follow the format
        :return: Dataframe with transactions
        """
        row_no = 0
        for index, row in transactions_df.iterrows():
            date_string = [int(i) for i in row['Date'].split('-')]
            row['Date'] = list_to_date(date_string)
            transactions_df.iat[row_no, 1] = row['Date']
            row_no += 1
        return transactions_df

    @staticmethod
    def validate_transactions(transactions_df):
        """
        Verify if the values in the transaction file are valid

        :param transactions_df: csv file with transactions, follow the format
        :return: Dataframe with transactions
        """
        for index, row in transactions_df.iterrows():
            if not(row['Date'] <= date.today() and
                   row['Price'] > 0 and
                   row['Quantity'] != 0):
                print("Please, fix your transaction info")
                raise NameError('InvalidTransactionInfo')

    @staticmethod
    def sort_transactions(transactions_df):
        """
        Sort the Dataframe by Date

        :param transactions_df: csv file with transactions, follow the format
        :return: Dataframe with transactions
        """
        return transactions_df.sort_values(by='Date')


def get_transactions_number(transactions_df):
    return len(transactions_df)


def list_to_date(trading_date):
    return date(int(trading_date[0]), int(trading_date[1]), int(trading_date[2]))


def main():

    # Create an instance of Transactions Utils
    transactions_list = TransactionsUtils("all", transaction_file_path)
    print("Number of transactions = " + str(get_transactions_number(transactions_list.get_transactions(date.today()))))

    transactions = transactions_list.get_transactions(date(2018, 1, 1))
    print("Transactions = ")
    print(str(transactions))

    period = transactions_list.get_transactions_period(date(2014, 1, 1), date(2014, 12, 31))
    print("Transactions in 2014 = ")
    print(str(period))


if __name__ == '__main__':
    main()
