# -------------------------------------------------------------------------------
# Name:         share_utils
# Purpose:      Class with methods for share status snapshot in time
#
# Author:       Mathieu Guilbault
#
# Created:      2019-03-04
# Copyright:    (c) Mathieu Guilbault 2019
# -------------------------------------------------------------------------------
from historical_utils import HistoricalUtils
from transactions_utils import TransactionsUtils
from datetime import date


class ShareUtils:
    def __init__(self, ticker):
        self.ticker = ticker
        self.transactions = TransactionsUtils(self.ticker).get_transactions()
        self.historical = HistoricalUtils(self.ticker, date(2018, 1, 1))

    def get_transactions(self):
        return self.transactions

    def get_transactions_number(self):
        pass

    # def set_share_nb(self):
    #     return self.transactions['Quantity'].sum()
    #
    # def set_total_cost(self):
    #     total_cost = 0
    #     for index, row in self.transactions.iterrows():
    #         total_cost = total_cost + row['Price'] * row['Quantity'] + row['Commission']
    #     return total_cost
    #
    # def set_mean_cost(self):
    #     if self.share_nb == 0:
    #         return 0
    #     else:
    #         return "{:.2f}".format(self.total_cost / self.share_nb)

    def get_actual_price(self, market_date):
        return self.historical.get_close_price(market_date)


def main():

    # Create an instance of Transactions Utils
    share = ShareUtils("VUS.TO")

    print("Actual price = " + str(share.get_actual_price(date(2019, 7, 5))))


if __name__ == '__main__':
    main()
