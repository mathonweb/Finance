from datetime import datetime

from pytz import timezone

import config


def find_errors_in_logs(filename):
    today_date = datetime.now(timezone('US/Eastern')).strftime("%Y-%m-%d")
    with open(filename) as f:
        for line in f:
            if line.find("ERROR") != -1 and line.find(today_date) != -1:
                return True
    f.close()

    return False


if __name__ == '__main__':
    return_val = find_errors_in_logs('../logs.log')
    print(return_val)
