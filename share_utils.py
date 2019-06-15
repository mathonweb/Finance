# -------------------------------------------------------------------------------
# Name:         share_utils
# Purpose:      Class with methods for share status snapshot in time
#
# Author:       Mathieu Guilbault
#
# Created:      2019-03-04
# Copyright:    (c) Mathieu Guilbault 2019
# -------------------------------------------------------------------------------


class ShareUtils:
    def __init__(self, transactions_df, ticker, date):
        self.ticker = ticker
        self.date = date
        self.transactions = self.get_transactions(transactions_df)
        self.share_nb = self.get_share_nb()
        self.total_cost = self.get_total_cost()
        self.mean_cost = self.get_mean_cost()
        self.actual_price = 0
        self.market_value = 0
        self.profit = 0
        self.pourcentage_profit = 0

    def get_transactions(self, transactions_df):
        all_transactions = transactions_df.loc[self.ticker]
        return all_transactions[all_transactions['Date'] <= self.date]

    def get_share_nb(self):
        return self.transactions['Quantity'].sum()

    def get_total_cost(self):
        total_cost = 0
        for index, row in self.transactions.iterrows():
            total_cost = total_cost + row['Price'] * row['Quantity'] + row['Commission']
        return total_cost

    def get_mean_cost(self):
        return "{:.2f}".format(self.total_cost / self.share_nb)
