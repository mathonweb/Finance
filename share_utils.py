from datetime import date
from historical_utils import HistoricalUtils
from transactions_utils import TransactionsUtils


class ShareUtils:
    def __init__(self, ticker):
        self.ticker = ticker
        self.transactions = TransactionsUtils(self.ticker).get_transactions()
        self.historical = HistoricalUtils(self.ticker, date(2018, 1, 1))

    def get_transactions(self):
        return self.transactions

    def get_transactions_number(self):
        pass

    # def get_share_nb(self, market_date):
    #     return self.transactions['Quantity'].sum()
    #
    # def get_total_cost(self, market_date):
    #     total_cost = 0
    #     for index, row in self.transactions.iterrows():
    #         total_cost = total_cost + row['Price'] * row['Quantity'] + row['Commission']
    #     return total_cost
    #
    # def get_mean_cost(self, market_date):
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
