import os
from datetime import date
from pathlib import Path

import pandas as pd
from yahoo_historical import Fetcher

from config import historical_files_path
from lib_utils import format_dates, string_to_date, date_to_list

INVESTING_FIRST_DATE = date(2012, 1, 1)


class HistoricalUtils:
    """
    Historical dataframe related to a ticker and methods to get info on the ticker
    """
    def __init__(self, ticker):
        self.ticker = ticker
        self.historical_df = self.set_historical(ticker)

    @staticmethod
    def set_historical(ticker):
        """
        Get the ticker historical data up to today

        :param ticker: ticker name (Ex: CIF.TO)
        :return: dataframe of ticker's historical data
        """

        market_date = date.today()

        # Verify if the csv file is already present
        file_name = os.path.join(historical_files_path, ticker + ".csv")
        if Path(file_name).is_file():
            historical_df = pd.read_csv(file_name, skip_blank_lines=True, index_col=False)
        else:
            historical_df = Fetcher(ticker, date_to_list(INVESTING_FIRST_DATE), date_to_list(market_date)).\
                get_historical()
            historical_df.to_csv(file_name)

        # Verify if dates are covered by the start date and end date
        min_date_string = historical_df["Date"].iloc[0]
        min_date = string_to_date(min_date_string)
        max_date_string = historical_df["Date"].iloc[-1]
        max_date = string_to_date(max_date_string)

        # If market date is out of bound, download the historical data from Yahoo
        if market_date < min_date:
            historical_df = Fetcher(ticker, date_to_list(market_date), date_to_list(max_date)).\
                get_historical()
        if market_date > max_date:
            historical_df = Fetcher(ticker, date_to_list(min_date), date_to_list(market_date)).\
                get_historical()

        # Create a csv file with the data
        historical_df.to_csv(file_name)

        historical_df = format_dates(historical_df)
        historical_df.rename(columns={'Date': "Market_date"})
        historical_df.set_index("Market_date")
        return historical_df

    def get_market_date(self, req_date):
        """
        Get the market date closest to the requested date.

        :param req_date: Date that we want historical data
        :return: Market date closest to the requested date
        """
        return max(filter(lambda x: x <= req_date, self.historical_df["Date"]))

    def _get_item(self, req_date, item):
        """


        :param req_date:
        :param item:
        :return:
        """
        market_date = self.get_market_date(req_date)
        item_value = self.historical_df.loc[market_date.strftime("%d-%m-%Y"), item]
        # item_value = 0
        # for index, row in self.historical_df.iterrows():
        #     if row["Date"] == market_date:
        #         item_value = row[item]
        return item_value

    def get_open_price(self, trading_date):
        return self._get_item(trading_date, 'Open')

    def get_high_price(self, trading_date):
        return self._get_item(trading_date, 'High')

    def get_low_price(self, trading_date):
        return self._get_item(trading_date, 'Low')

    def get_close_price(self, trading_date):
        return self._get_item(trading_date, 'Close')

    def get_adj_close_price(self, trading_date):
        return self._get_item(trading_date, 'Adj Close')

    def get_volume(self, trading_date):
        return self._get_item(trading_date, 'Volume')


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
