# -------------------------------------------------------------------------------
# Name:         share_utils
# Purpose:      Class with methods for share status snapshot in time
#
# Author:       Mathieu Guilbault
#
# Created:      2019-03-04
# Copyright:    (c) Mathieu Guilbault 2019
# -------------------------------------------------------------------------------
import pandas as pd


class ShareUtils:
    def __init__(self, transactions_df, historical_df, ticker, date):
        self.ticker = ticker
        self.date = date
        self.transactions = self.get_transactions(transactions_df)
        self.transactions_number = self.get_transactions_number()
        self.share_nb = self.get_share_nb()
        self.total_cost = self.get_total_cost()
        self.mean_cost = self.get_mean_cost()
        self.actual_price = self.get_actual_price(historical_df)
        self.market_value = 0
        self.profit = 0
        self.pourcentage_profit = 0

    def get_transactions(self, transactions_df):
        all_transactions = pd.DataFrame(transactions_df.loc[self.ticker])
        print(all_transactions)
        # Problem - Does not support 1 line DataFrame
        return all_transactions[all_transactions['Date'] <= self.date]

    def get_transactions_number(self):
        return len(self.transactions.index)

    def get_share_nb(self):
        return self.transactions['Quantity'].sum()

    def get_total_cost(self):
        total_cost = 0
        for index, row in self.transactions.iterrows():
            total_cost = total_cost + row['Price'] * row['Quantity'] + row['Commission']
        return total_cost

    def get_mean_cost(self):
        if self.share_nb == 0:
            return 0
        else:
            return "{:.2f}".format(self.total_cost / self.share_nb)

    def get_actual_price(self, historical_df):
        idx = historical_df['Date'].sub(self.date).abs().idxmin()
        return historical_df.at[idx, 'Close']
