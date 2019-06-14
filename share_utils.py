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
    def __init__(self, transactions_df, historical_df, ticker, date):
        self.ticker = ticker
        self.date = date
        self.share_nb = 0
        self.mean_cost = 0
        self.total_cost = 0
        self.actual_price = 0
        self.market_value = 0
        self.profit = 0
        self.pourcentage_profit = 0

    def get_share_nb(self, transactions_df):
        """
        :param transaction_date:
        :return:
        """

        for index, row in self.transactions_df.iterrows():
            if row['Ticker'] == self.ticker:

        #share_nb = 0
        #for transaction in self.transactions:
        #    if transaction[TRANSACTION_DATE] <= transaction_date:
        #        share_nb += transaction[NUMBER]
        #
        #return share_nb

    def get_mean_cost(self, transactions_df):
        """
        :param transaction_date:
        :return:
        """
        self.mean_cost = 0

        #total_cost = 0
        #for transaction in self.transactions:
        #    if transaction[TRANSACTION_DATE] <= transaction_date:
        #        if transaction[NUMBER] > 0:
        #            # Add the total price and the commission
        #            total_cost = total_cost + transaction[PRICE] * transaction[NUMBER] + transaction[COMMISSION]
        #mean_cost = total_cost / self.get_share_nb(transaction_date)
        #
        #return mean_cost