# -------------------------------------------------------------------------------
# Name:         transactions_utils
# Purpose:      Create a dataframes with all transactions
#               Return info from the transactions
#
# Author:       Mathieu Guilbault
#
# Created:      2019-03-04
# Copyright:    (c) Mathieu Guilbault 2019
# -------------------------------------------------------------------------------
from datetime import date
import os
import pandas as pd


class TransactionsUtils:
    def __init__(self, ticker):
        self.file = self.set_file()
        self.ticker = ticker
        self.transactions_df = pd.DataFrame()
        self.set_transactions()

    def set_file(self):
        # Read the transactions.txt file if exists
        try:
            return str(os.environ['INVESTING_PATH']) + "\\" + "transactions.csv"
        except Exception as e:
            print(e)

    def set_transactions(self):
        # Create a pandas dataframe
        #    Ticker   Date        Price   Quantity    Commission
        # 0  XEF.TO   01/01/2017  10.9    5         9.99

        transactions_df = pd.read_csv(self.file)
        if self.ticker is not "all":
            self.transactions_df = transactions_df.loc[transactions_df['Ticker'] == self.ticker]
        else:
            self.transactions_df = transactions_df
        self.format_dates()
        self.validate_transactions()
        self.sort_transactions()

    def format_dates(self):
        row_no = 0
        for index, row in self.transactions_df.iterrows():
            # Convert Excel date format into Date format
            date_string = [int(i) for i in row['Date'].split('-')]
            row['Date'] = self.list_to_date(date_string)
            self.transactions_df.iat[row_no, 1] = row['Date']
            row_no += 1

    def list_to_date(self, trading_date):
        return date(int(trading_date[0]), int(trading_date[1]), int(trading_date[2]))

    def validate_transactions(self):
        for index, row in self.transactions_df.iterrows():
            if not(row['Date'] <= date.today() and
                   row['Price'] > 0 and
                   row['Quantity'] != 0):
                print("Please, fix your transaction info")
                raise NameError('InvalidTransactionInfo')

    def sort_transactions(self):
        self.transactions_df.sort_values(by='Date')

    def get_transactions(self, market_date):
        if date is None:
            return self.transactions_df
        else:
            return self.transactions_df[self.transactions_df['Date'] <= market_date]

    def get_transactions_number(self):
        return len(self.transactions_df)

    def get_tickers(self):
        return self.ticker


def main():

    # Create an instance of Transactions Utils
    transactions_list = TransactionsUtils("XEF.TO")
    print("Number of transactions = " + str(transactions_list.get_transactions_number()))

    transactions = transactions_list.get_transactions(date(2018, 1, 1))
    print("Transactions = " + str(transactions))


if __name__ == '__main__':
    main()
