# -------------------------------------------------------------------------------
# Name:         share
# Purpose:      Class defining a share components
#
# Author:       Mathieu Guilbault
#
# Created:      2019-02-10
# Copyright:    (c) Mathieu Guilbault 2019
# -------------------------------------------------------------------------------

from datetime import date

# Contains the transaction informations related to a specific share


class Share:
    def __init__(self, transaction_date, price, number, commission):
        # Validate the transaction date
        validate_date(transaction_date)
        # Validate the price
        validate_price(price)
        # Validate the commission
        validate_price(commission)
        self.transactions = [[transaction_date, price, number, commission]]

    def add_transaction(self, transaction_date, price, number, commission):
        """
        :param transaction_date:
        :param price:
        :param number:
        :param commission:
        :return:
        """

        # Validate the transaction date
        validate_date(transaction_date)

        # Validate the price
        validate_price(price)

        # Validate the commission
        validate_price(commission)

        self.transactions.append([transaction_date, price, number, commission])
        self.transactions.sort()

        return True

    def remove_transaction(self, transaction_date):
        """
        :param transaction_date:
        :return:
        """
        # Validate the transaction date
        validate_date(transaction_date)

        index2delete = list()
        for transaction in self.transactions:
            if transaction[0] == transaction_date:
                index2delete.append(transaction)
        deleted_transaction_count = len(index2delete)

        if deleted_transaction_count > 1:
            raise NameError('MultipleRemove')
            return False

        del self.transactions[self.transactions.index(index2delete[0])]

        return True

    def get_transaction(self, transaction_date):
        """
        :param transaction_date:
        :return:
        """
        # Validate the transaction date
        validate_date(transaction_date)

        index2return = list()
        for transaction in self.transactions:
            if transaction[0] == transaction_date:
                index2return.append(transaction)
        index_to_return_count = len(index2return)

        if index_to_return_count == 0:
            raise NameError('MissingTransaction')
            return False
        if index_to_return_count > 1:
            raise NameError('MultipleGet')
            return False

        return self.transactions[self.transactions.index(index2return[0])]


def validate_date(date_to_validate):
    if date_to_validate > date.today():
        raise NameError('InvalidTransactionDate')
        return False


def validate_price(price_to_validate):
    if price_to_validate < 0:
        raise NameError('InvalidPrice')
        return False
