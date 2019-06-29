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
        self.format_date()

    def read_historical(self, ticker, start_date, end_date):

        # Verify if the csv file is not already present
        file_name = str(os.environ['INVESTING_PATH']) + "\\" + "Historical_data" + "\\" + ticker + ".csv"
        if Path(file_name).is_file():
            historical_df = pd.read_csv(file_name)

            # Verify if dates are covered by the start date and end date
            min_date_string = historical_df["Date"].iloc[0].split('-')
            min_date = date(int(min_date_string[0]), int(min_date_string[1]), int(min_date_string[2]))
            max_date_string = historical_df["Date"].iloc[-1].split('-')
            max_date = date(int(max_date_string[0]), int(max_date_string[1]), int(max_date_string[2]))

            if date(start_date[0], start_date[1], start_date[2]) >= min_date and date(end_date[0], end_date[1],
                                                                                      end_date[2]) <= max_date:
                # Set possible start date
                self.start_date = min_date
                # Set possible end date
                self.end_date = max_date

                self.historical_df = historical_df

                return 0

        # If not, download the historical data from Yahoo
        historical_df = Fetcher(ticker, start_date, end_date).getHistorical()

        # Create a csv file with the data
        historical_df.to_csv(file_name)

        self.historical_df = historical_df

    def format_date(self):
        row_no = 0
        for index, row in self.historical_df.iterrows():
            # Convert Excel date format into list of integers
            date_string = [int(i) for i in row['Date'].split('-')]
            row['Date'] = date(date_string[0], date_string[1], date_string[2])
            self.historical_df.iloc[row_no] = row
            row_no += 1

    def get_date(self):
        pass

    def get_open_price(self, date):
        pass

    def get_high_price(self, date):
        pass

    def get_low_price(self, date):
        pass

    def get_close_price(self, date):
        pass

    def get_adj_close_price(self, date):
        pass

    def get_volume(self, date):
        pass


def main():

    # Create an instance of Historical Utils
    historical_list = HistoricalUtils("VUS.TO", [2012, 1, 24], [2019, 1, 1])


if __name__ == '__main__':
    main()
