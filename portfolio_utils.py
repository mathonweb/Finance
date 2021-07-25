from datetime import date

import pandas as pd

from historical_utils import HistoricalUtils
from transactions_utils import TransactionsUtils


class PortfolioUtils:
    """
    Contains asset at a specific date
    """
    def __init__(self, trading_date):
        self.trading_date = trading_date
        self.portfolio = self._set_portfolio()

    def _set_portfolio(self):
        """
        Set assets in a dataframe for a specific date

        :return: Asset portfolio dataframe
        """
        # Get transactions up to the trading date
        transactions_inst = TransactionsUtils("all")
        transactions = transactions_inst.get_transactions(self.trading_date)

        portfolio = pd.DataFrame(index=None, columns={"Ticker", "Mean cost", "Quantity", "Commission", "Price"})

        ticker_index = None
        mean_cost = None

        # Get portfolio status at that date
        for index, row in transactions.iterrows():
            # Check if the ticker already exists
            ticker_index = self._find_ticker(row["Ticker"], portfolio)
            # Add the ticker in the Dataframe if it not exists in the portfolio
            if ticker_index is None:
                portfolio = portfolio.append({"Ticker": row["Ticker"], "Mean cost": 0, "Quantity": 0,
                                              "Commission": 0}, ignore_index=True)
                ticker_index = self._find_ticker(row["Ticker"], portfolio)

            # Update the mean price, the quantity and the commission
            cost = portfolio.loc[ticker_index, "Mean cost"]
            quantity = portfolio.loc[ticker_index, "Quantity"]
            total_quantity = quantity + row["Quantity"]
            if row["Quantity"] > 0:
                mean_cost = cost * quantity / total_quantity + row["Price"] * row["Quantity"] / total_quantity
            else:
                mean_cost = cost
            portfolio.loc[ticker_index, "Mean cost"] = mean_cost
            # Sum the quantity
            portfolio.loc[ticker_index, "Quantity"] = total_quantity
            # Add the commission
            portfolio.loc[ticker_index, "Commission"] += row["Commission"]

            # I prefer to keep the ticker with empty quantity to keep trace on Commission

        if portfolio.size > 0:
            # Round the total Mean cost
            portfolio.loc[ticker_index, "Mean cost"] = round(mean_cost, 2)

            # Complete with the closed price
            for index, row in portfolio.iterrows():
                if row["Quantity"] > 0:
                    portfolio.loc[index, "Price"] = HistoricalUtils(row["Ticker"]).get_close_price(self.trading_date)

        return portfolio

    @staticmethod
    def _find_ticker(ticker, portfolio):
        """
        Find the ticker in the portfolio

        :param ticker: Ticker name
        :param portfolio: Asset portfolio
        :return: Index in the portfolio where the ticker is located
        """
        for index, row in portfolio.iterrows():
            if row["Ticker"] == ticker:
                return index

        return None

    def get_portfolio(self):
        """
        Return the Asset portfolio

        :return: Asset portfolio
        """
        return self.portfolio


def calculate_value(calendar_date):
    """
    Calculate the Asset portfolio value at a specific date

    :param calendar_date: Date
    :return: Assets total value
    """
    portfolio_on_date = PortfolioUtils(calendar_date).get_portfolio()

    value = 0
    for index, row in portfolio_on_date.iterrows():
        if row["Quantity"] > 0:
            value += row["Price"] * row["Quantity"]

    return value


def main():
    # Create an instance of Portfolio Utils
    portfolio = PortfolioUtils(date(2020, 1, 1))
    print(portfolio.get_portfolio())


if __name__ == '__main__':
    main()
