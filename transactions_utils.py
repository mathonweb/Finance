# -------------------------------------------------------------------------------
# Name:         transactions_utils
# Purpose:      Create the objects associated to every quotes
#               Manage the transactions
#               Create or update the transactions sheet
#
# Author:       Mathieu Guilbault
#
# Created:      2019-03-04
# Copyright:    (c) Mathieu Guilbault 2019
# -------------------------------------------------------------------------------
from datetime import date
from share_utils import ShareUtils


def main():

    fnb1 = ShareUtils(date(2014, 1, 1), 10, 10, 9.99)
    fnb1.add_transaction(date(2017, 1, 1), 20, 5, 9.99)
    fnb1.add_transaction(date(2018, 1, 1), 30, 7, 9.99)
    fnb1.add_transaction(date(2019, 1, 1), 30, 9, 9.99)

    for transaction in fnb1.transactions:
        print(transaction)

    fnb1.remove_transaction(date(2018, 1, 1))

    print("After transaction deletion")
    try:
        for transaction in fnb1.transactions:
            print(transaction)
    except Exception as e:
        print(e)

    last_transaction = fnb1.get_transaction(date(2017, 1, 1))

    print("Last transaction = ", last_transaction)

    nb_of_shares = fnb1.get_share_nb(date(2019, 1, 1))

    print("Nb of shares = ", nb_of_shares)

    mean_cost = fnb1.get_mean_cost(date(2019, 1, 1))

    print("Mean cost = {0:.2f}".format(mean_cost))


if __name__ == '__main__':
    main()
