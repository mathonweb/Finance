from datetime import date, datetime


def format_dates(df):
    df['Date'] = [datetime.strptime(i, '%Y-%m-%d').date() for i in df['Date']]
    return df


def string_to_date(trading_date):
    trading_date_split = trading_date.split('-')
    return date(int(trading_date_split[0]), int(trading_date_split[1]), int(trading_date_split[2]))


def list_to_date(trading_date):
    return date(int(trading_date[0]), int(trading_date[1]), int(trading_date[2]))


def date_to_list(trading_date):
    return [trading_date.year, trading_date.month, trading_date.day]