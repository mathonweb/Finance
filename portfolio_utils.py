# -------------------------------------------------------------------------------
# Name:         portfolio_utils
# Purpose:      Class with methods for portfolio manipulation
#
# Author:       Mathieu Guilbault
#
# Created:      2019-07-12
# Copyright:    (c) Mathieu Guilbault 2019
# -------------------------------------------------------------------------------
from datetime import date
import pandas as pd
from transactions_utils import TransactionsUtils


class PortfolioUtils:
    def __init__(self, trading_date):
        self.date = trading_date
        self.transactions = TransactionsUtils("all").get_transactions(trading_date)
        self.portfolio = pd.DataFrame(index=None, columns={"Ticker", "Mean price", "Quantity", "Commission"})
        self.set_portfolio()

    def set_portfolio(self):

        # Get portfolio status at that date
        for index, row in self.transactions.iterrows():
            # Add the ticker in the Dataframe if it is not present
            ticker_index = self.find_ticker(row["Ticker"])
            if ticker_index is None:
                self.portfolio = self.portfolio.append({"Ticker": row["Ticker"], "Mean price": 0, "Quantity": 0,
                                                        "Commission": 0}, ignore_index=True)
            ticker_index = self.find_ticker(row["Ticker"])

            # Set the Mean Price
            price = self.portfolio.loc[ticker_index, "Mean price"]
            quantity = self.portfolio.loc[ticker_index, "Quantity"]
            total_quantity = quantity + row["Quantity"]
            mean_price = price*quantity/total_quantity + row["Price"]*row["Quantity"]/total_quantity
            self.portfolio.loc[ticker_index, "Mean price"] = mean_price
            # Sum the quantity
            self.portfolio.loc[ticker_index, "Quantity"] = total_quantity
            # Add the commission
            self.portfolio.loc[ticker_index, "Commission"] += row["Commission"]
        # If quantity is 0 for a ticker, remove it from the portfolio

    def find_ticker(self, ticker):
        for index, row in self.portfolio.iterrows():
            if row["Ticker"] == ticker:
                return index

        return None

    def get_portfolio(self):
        return self.portfolio


def main():

    # Create an instance of Portfolio Utils
    portfolio = PortfolioUtils(date(2019, 1, 1)).get_portfolio()
    print(portfolio)


if __name__ == '__main__':
    main()