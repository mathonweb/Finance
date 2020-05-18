from datetime import date


def format_dates(df):
    row_no = 0
    for index, row in df.iterrows():
        # Convert Excel date format into Date format
        date_string = [int(i) for i in row['Date'].split('-')]
        row['Date'] = list_to_date(date_string)
        df.iat[row_no, 1] = row['Date']
        row_no += 1
    return df


def string_to_date(trading_date):
    trading_date_split = trading_date.split('-')
    return date(int(trading_date_split[0]), int(trading_date_split[1]), int(trading_date_split[2]))


def list_to_date(trading_date):
    return date(int(trading_date[0]), int(trading_date[1]), int(trading_date[2]))


def date_to_list(trading_date):
    return [trading_date.year, trading_date.month, trading_date.day]