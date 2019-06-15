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
    def __init__(self, file):
        self.transactions_df = self.read_transactions(file)
        self.format_date()
        self.validate_transactions()
        self.sort_transactions()

    def read_transactions(self, file):
        # Create a pandas dataframe
        #    Ticker   Date        Price   Quantity    Commission
        # 0  XEF.TO   01/01/2017  10.9    5         9.99

        transactions_df = pd.read_csv(file, index_col="Ticker")
        return transactions_df

    def format_date(self):
        row_no = 0
        for index, row in self.transactions_df.iterrows():
            # Convert Excel date format into list of integers
            date_string = [int(i) for i in row['Date'].split('/')]
            row['Date'] = date(date_string[2], date_string[1], date_string[0])
            self.transactions_df.iloc[row_no] = row
            row_no += 1

    def validate_transactions(self):
        for index, row in self.transactions_df.iterrows():
            if not(row['Date'] <= date.today() and
                   row['Price'] > 0 and
                   row['Quantity'] != 0):
                raise NameError('InvalidTransactionInfo')
                print("Please, fix your transaction info")
                exit(1)

    def sort_transactions(self):
        self.transactions_df.sort_values(by='Date')

    def get_transactions(self):
        return self.transactions_df

    def get_transactions_number(self):
        return len(self.transactions_df)


def main():

    # Read the transactions.txt file if exist, otherwise create it
    try:
        file = str(os.environ['TRANSACTIONS_PATH']) + "\\" + "transactions.csv"
    except Exception as e:
        print(e)

    # Create an instance of Transactions Utils
    transactions_list = TransactionsUtils(file)

    print(transactions_list.get_transactions_number())


if __name__ == '__main__':
    main()
