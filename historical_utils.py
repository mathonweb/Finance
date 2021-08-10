from datetime import date
from pathlib import Path

import pandas as pd
import yfinance

from utils.logger import logger

INVESTING_FIRST_DATE = date(2012, 1, 1)


def _get_historical_data(ticker):
    """
    Get historical data for a ticker from yahoo finance website
    :param ticker: Ticker name (Ex: CIF.TO)
    """
    file_name = Path(ticker + ".csv")
    try:
        historical_df = yfinance.download(ticker, INVESTING_FIRST_DATE)
        historical_df.to_csv(file_name)
    except Exception as e:
        logger.error("Not possible to get historical data from yahoo finance:" + str(file_name))


class HistoricalUtils:
    """
    Historical dataframe related to a ticker and methods to get info on the ticker
    """
    def __init__(self, ticker):
        self._historical_df = self._set_historical(ticker)

    @staticmethod
    def _set_historical(ticker):
        """
        Get the ticker historical data up to today

        :param ticker: ticker name (Ex: CIF.TO)
        :return: dataframe of ticker's historical data
        """

        # Verify if the csv file is already present
        file_name = Path(ticker + ".csv")

        if not file_name.is_file():
            _get_historical_data(ticker)

        else:
            historical_df = pd.read_csv(file_name, skip_blank_lines=True, index_col=None, usecols=["Date", "Open",
                                                                                                   "High", "Low",
                                                                                                   "Close",
                                                                                                   "Adj Close",
                                                                                                   "Volume"])
            historical_last_day = date.fromisoformat(historical_df['Date'].iloc[-1])

            # Update the historical csv file if it is outdated
            if date.today().isoweekday() and date.today() > historical_last_day:
                _get_historical_data(ticker)

        historical_df = pd.read_csv(file_name, skip_blank_lines=True, index_col=None, usecols=["Date", "Open",
                                                                                               "High", "Low",
                                                                                               "Close",
                                                                                               "Adj Close",
                                                                                               "Volume"])

        return historical_df

    def get_market_date(self, req_date):
        """
        Get the market date closest to the requested date.

        :param req_date: Date that we want historical data
        :return: Market date closest to the requested date
        """
        return max(filter(lambda x: date.fromisoformat(x) <= req_date, self._historical_df['Date']))

    def _get_item(self, req_date, item):
        """
        Get column value at a specific date

        :param req_date: Request date of the value to get
        :param item: Column name of the value to get
        :return: Column-row value
        """

        closest_date = self.get_market_date(req_date)
        item_value = 0
        for index, row in self._historical_df.iterrows():
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
