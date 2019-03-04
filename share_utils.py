# -------------------------------------------------------------------------------
# Name:         share_utils
# Purpose:      Class with methods for share status snapshot in time
#
# Author:       Mathieu Guilbault
#
# Created:      2019-03-04
# Copyright:    (c) Mathieu Guilbault 2019
# -------------------------------------------------------------------------------

from share import Share
from share import validate_date

# Contains method for share status snapshot in time


class ShareUtils(Share):
    def __init__(self, transaction_date, price, number, commission):
        Share.__init__(self, transaction_date, price, number, commission)

    def get_mean_cost(self, transaction_date):
        """
        :param transaction_date:
        :return:
        """
        # Validate the transaction date
        validate_date(transaction_date)

        total_cost = 0
        for transaction in self.transactions:
            if transaction[0] <= transaction_date:
                if transaction[2] > 0:
                    # Add the total price and the commission
                    total_cost = total_cost + transaction[1] * transaction[2] + transaction[3]
        mean_cost = total_cost / self.get_share_nb(transaction_date)

        return mean_cost

    def get_share_nb(self, transaction_date):
        """
        :param transaction_date:
        :return:
        """

        # Validate the transaction date
        validate_date(transaction_date)

        share_nb = 0
        for transaction in self.transactions:
            if transaction[0] <= transaction_date:
                share_nb += transaction[2]

        return share_nb
