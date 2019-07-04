# -------------------------------------------------------------------------------
# Name:         historical_utils
# Purpose:      Create a dataframes from historical data
#               Return info from historical data
#
# Author:       Mathieu Guilbault
#
# Created:      2019-06-15
# Copyright:    (c) Mathieu Guilbault 2019
# -------------------------------------------------------------------------------
import os
from datetime import date
from pathlib import Path

import pandas as pd
# https://github.com/AndrewRPorter/yahoo-historical
from yahoo_historical import Fetcher


class HistoricalUtils:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.historical_df = ""
        self.start_date = ""
        self.end_date = ""
        self.read_historical(ticker, start_date, end_date)
        self.format_dates()

    def read_historical(self, ticker, start_date, end_date):

        # Verify if the csv file is not already present
        file_name = str(os.environ['INVESTING_PATH']) + "\\" + "Historical_data" + "\\" + ticker + ".csv"
        if Path(file_name).is_file():
            historical_df = pd.read_csv(file_name)

            # Verify if dates are covered by the start date and end date
            min_date_string = historical_df["Date"].iloc[0]
            min_date = self.string_to_date(min_date_string)
            max_date_string = historical_df["Date"].iloc[-1]
            max_date = self.string_to_date(max_date_string)

            if start_date >= min_date and end_date <= max_date:
                # Set possible start date
                self.start_date = min_date
                # Set possible end date
                self.end_date = max_date

                self.historical_df = historical_df

                return 0

        # If not, download the historical data from Yahoo
        historical_df = Fetcher(ticker, self.date_to_list(start_date), self.date_to_list(end_date)).getHistorical()

        # Create a csv file with the data
        historical_df.to_csv(file_name)

        self.historical_df = historical_df

    def format_dates(self):
        row_no = 0
        for index, row in self.historical_df.iterrows():
            # Convert Excel date format into list of integers
            date_string = [int(i) for i in row['Date'].split('-')]
            row['Date'] = self.list_to_date(date_string)
            self.historical_df.loc[row_no] = row
            row_no += 1

    def string_to_date(self, trading_date):
        trading_date_split = trading_date.split('-')
        return date(int(trading_date_split[0]), int(trading_date_split[1]), int(trading_date_split[2]))

    def list_to_date(self, trading_date):
        return date(int(trading_date[0]), int(trading_date[1]), int(trading_date[2]))

    def date_to_list(self, trading_date):
        return [trading_date.year, trading_date.month, trading_date.day]

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_closest_date(self, trading_date):
        return max(filter(lambda x: x <= trading_date, self.historical_df["Date"]))

    def get_item(self, trading_date, item):
        closest_date = self.get_closest_date(trading_date)
        item_value = 0
        for index, row in self.historical_df.iterrows():
            if row["Date"] == closest_date:
                item_value = row[item]
        return item_value

    def get_open_price(self, trading_date):
        return self.get_item(trading_date, 'Open')

    def get_high_price(self, trading_date):
        return self.get_item(trading_date, 'High')

    def get_low_price(self, trading_date):
        return self.get_item(trading_date, 'Low')

    def get_close_price(self, trading_date):
        return self.get_item(trading_date, 'Close')

    def get_adj_close_price(self, trading_date):
        return self.get_item(trading_date, 'Adj Close')

    def get_volume(self, trading_date):
        return self.get_item(trading_date, 'Volume')


def main():

    # Create an instance of Historical Utils
    historical_list = HistoricalUtils("VUS.TO", date(2012, 1, 24), date(2019, 2, 27))

    closest_date = historical_list.get_closest_date(date(2012, 4, 5))
    print("Closest date = " + str(closest_date))
    print("Open price = " + str(historical_list.get_open_price(closest_date)))
    print("High price = " + str(historical_list.get_high_price(closest_date)))
    print("Low price = " + str(historical_list.get_low_price(closest_date)))
    print("Close price = " + str(historical_list.get_close_price(closest_date)))
    print("Adjusted closed price = " + str(historical_list.get_adj_close_price(closest_date)))
    print("Volume = " + str(historical_list.get_volume(closest_date)))


if __name__ == '__main__':
    main()
