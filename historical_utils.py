import os
from datetime import date
from pathlib import Path

import pandas as pd
import yfinance

from config import historical_files_path
from utils.logger import logger

INVESTING_FIRST_DATE = date(2012, 1, 1)


class HistoricalUtils:
    """
    Historical dataframe related to a ticker and methods to get info on the ticker
    """
    def __init__(self, ticker):
        self.ticker = ticker
        self.historical_df = self._set_historical(ticker)

    @staticmethod
    def _set_historical(ticker):
        """
        Get the ticker historical data up to today

        :param ticker: ticker name (Ex: CIF.TO)
        :return: dataframe of ticker's historical data
        """

        market_date = date.today()

        # Verify if the csv file is already present
        file_name = os.path.join(historical_files_path, ticker + ".csv")
        if Path(file_name).is_file():
            historical_df = pd.read_csv(file_name, skip_blank_lines=True, index_col=None, usecols=["Date", "Open",
                                                                                                   "High", "Low",
                                                                                                   "Close",
                                                                                                   "Adj Close",
                                                                                                   "Volume"])
        else:
            try:
                historical_df = yfinance.download(ticker, INVESTING_FIRST_DATE, market_date)
                historical_df.to_csv(file_name)
            except Exception as e:
                logger.error("Not possible to get historical data from internet:" + str(e))

        # Verify if dates are covered by the start date and end date
        min_date = date.fromisoformat(historical_df["Date"].iloc[0])
        max_date = date.fromisoformat(historical_df["Date"].iloc[-1])

        # If market date is out of bound, download the historical data from Yahoo
        if market_date < min_date:
            try:
                historical_df = yfinance.download(ticker, market_date, max_date)
                # Create a csv file with the data
                historical_df.to_csv(file_name)
            except Exception as e:
                logger.error("Not possible to get historical data from internet:" + str(e))
        if market_date > max_date:
            try:
                historical_df = yfinance.download(ticker, min_date, market_date)
                # Create a csv file with the data
                historical_df.to_csv(file_name)
            except Exception as e:
                logger.error("Not possible to get historical data from internet:" + str(e))

        historical_df["Date"] = historical_df.index

        return historical_df

    def get_market_date(self, req_date):
        """
        Get the market date closest to the requested date.

        :param req_date: Date that we want historical data
        :return: Market date closest to the requested date
        """
        return max(filter(lambda x: x <= req_date, self.historical_df['Date']))

    def _get_item(self, req_date, item):
        """
        Get column value at a specific date

        :param req_date: Request date of the value to get
        :param item: Column name of the value to get
        :return: Column-row value
        """

        closest_date = self.get_market_date(req_date)
        item_value = 0
        for index, row in self.historical_df.iterrows():
            if row["Date"] == closest_date:
                item_value = row[item]

        return item_value

    def get_open_price(self, trading_date):
        """
        Get the open price

        :param trading_date: Trading date
        :return: Open price
        """
        return self._get_item(trading_date, 'Open')

    def get_high_price(self, trading_date):
        """
        Get the High price

        :param trading_date: Trading date
        :return: High price
        """
        return self._get_item(trading_date, 'High')

    def get_low_price(self, trading_date):
        """
        Get the Low price

        :param trading_date: Trading date
        :return: Low price
        """
        return self._get_item(trading_date, 'Low')

    def get_close_price(self, trading_date):
        """
        Get the Close price

        :param trading_date: Trading date
        :return: Close price
        """
        return self._get_item(trading_date, 'Close')

    def get_adj_close_price(self, trading_date):
        """
        Get the Adjusted close price

        :param trading_date: Trading date
        :return: Adjust close price
        """
        return self._get_item(trading_date, 'Adj Close')

    def get_volume(self, trading_date):
        """
        Get the Volume

        :param trading_date: Trading date
        :return: Volume
        """
        return self._get_item(trading_date, 'Volume')


def date_to_list(trading_date):
    return [trading_date.year, trading_date.month, trading_date.day]


def main():

    # Create an instance of Historical Utils
    historical_list = HistoricalUtils("XSB.TO")

    closest_date = historical_list.get_market_date(date(2019, 9, 1))

    print("Open price = " + str(historical_list.get_open_price(closest_date)))
    print("High price = " + str(historical_list.get_high_price(closest_date)))
    print("Low price = " + str(historical_list.get_low_price(closest_date)))
    print("Close price = " + str(historical_list.get_close_price(closest_date)))
    print("Adjusted closed price = " + str(historical_list.get_adj_close_price(closest_date)))
    print("Volume = " + str(historical_list.get_volume(closest_date)))


if __name__ == '__main__':
    main()
