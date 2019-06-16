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
from datetime import date
import pandas as pd
from yahoo_historical import Fetcher


class HistoricalUtils:
    def __init__(self, ticker, start_date, end_date):
        self.historical_df = self.read_historical(ticker, start_date, end_date)
        self.format_date()

    def read_historical(self, ticker, start_date, end_date):

        historical_df = Fetcher(ticker, start_date, end_date).getHistorical()
        return historical_df

    def format_date(self):
        row_no = 0
        for index, row in self.historical_df.iterrows():
            # Convert Excel date format into list of integers
            date_string = [int(i) for i in row['Date'].split('-')]
            row['Date'] = date(date_string[0], date_string[1], date_string[2])
            self.historical_df.iloc[row_no] = row
            row_no += 1


def main():

    # Create an instance of Historical Utils
    historical_list = HistoricalUtils("VUS.TO", [2012, 1, 1], [2019, 1, 1])

    print(historical_list.historical_df)


if __name__ == '__main__':
    main()
