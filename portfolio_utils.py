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

from historical_utils import HistoricalUtils
from transactions_utils import TransactionsUtils


class PortfolioUtils:
    def __init__(self, trading_date):
        self.date = trading_date
        self.transactions = TransactionsUtils("all").get_transactions(trading_date)
        self.portfolio = pd.DataFrame(index=None, columns={"Ticker", "Mean cost", "Quantity", "Commission", "Price"})
        self.set_portfolio()
        self.cash = 0

    def set_portfolio(self):

        # Get portfolio status at that date
        for index, row in self.transactions.iterrows():
            # Add the ticker in the Dataframe if it is not present
            ticker_index = self.find_ticker(row["Ticker"])
            if ticker_index is None:
                self.portfolio = self.portfolio.append({"Ticker": row["Ticker"], "Mean cost": 0, "Quantity": 0,
                                                        "Commission": 0}, ignore_index=True)
            ticker_index = self.find_ticker(row["Ticker"])

            # Update the mean price, the quantity and the commission
            cost = self.portfolio.loc[ticker_index, "Mean cost"]
            quantity = self.portfolio.loc[ticker_index, "Quantity"]
            total_quantity = quantity + row["Quantity"]
            if row["Quantity"] > 0:
                mean_cost = cost * quantity / total_quantity + row["Price"] * row["Quantity"] / total_quantity
            else:
                mean_cost = cost
            self.portfolio.loc[ticker_index, "Mean cost"] = mean_cost
            # Sum the quantity
            self.portfolio.loc[ticker_index, "Quantity"] = total_quantity
            # Add the commission
            self.portfolio.loc[ticker_index, "Commission"] += row["Commission"]

            # I prefer to keep the ticker with empty quantity to keep trace on Commission

        if self.portfolio.size > 0:
            # Round the total Mean cost
            self.portfolio.loc[ticker_index, "Mean cost"] = round(mean_cost, 2)

            # Complete with the closed price
            for index, row in self.portfolio.iterrows():
                if row["Quantity"] > 0:
                    self.portfolio.loc[index, "Price"] = HistoricalUtils(row["Ticker"], self.date). \
                        get_close_price(self.date)

    def find_ticker(self, ticker):
        for index, row in self.portfolio.iterrows():
            if row["Ticker"] == ticker:
                return index

        return None

    def get_portfolio(self):
        return self.portfolio


def main():
    # Create an instance of Portfolio Utils
    portfolio = PortfolioUtils(date(2013, 1, 1))
    print(portfolio.get_portfolio())


if __name__ == '__main__':
    main()
