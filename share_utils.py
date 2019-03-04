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
from share import COMMISSION
from share import TRANSACTION_DATE
from share import NUMBER
from share import PRICE

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
            if transaction[TRANSACTION_DATE] <= transaction_date:
                if transaction[NUMBER] > 0:
                    # Add the total price and the commission
                    total_cost = total_cost + transaction[PRICE] * transaction[NUMBER] + transaction[COMMISSION]
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
            if transaction[TRANSACTION_DATE] <= transaction_date:
                share_nb += transaction[NUMBER]

        return share_nb
