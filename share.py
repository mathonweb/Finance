#-------------------------------------------------------------------------------
# Name:         share
# Purpose:      Class defining a share components
#
# Author:       Mathieu Guilbault
#
# Created:      2019-02-10
# Copyright:    (c) Mathieu Guilbault 2019
#-------------------------------------------------------------------------------

import datetime

# Describe the share class


class Share:
    def __init__(self, transaction_date, price, number):
        self.transactions = [[transaction_date, price, number]]

    def add_transaction(self, transaction_date, price, number):
        # Validate the transaction date
        if transaction_date > datetime.date.today():
            raise NameError('InvalidTransactionDate')
            return
        # Validate the price
        if price < 0:
            raise NameError('InvalidPrice')
            return
        # Validate the number of share
        if number < 0:
            raise NameError('InvalidNumberOfShare')
            return

        self.transactions.append([transaction_date, price, number])
        self.transactions.sort()

    def remove_transaction(self, transaction_date):
        # Validate the transaction date
        if transaction_date > datetime.date.today():
            raise NameError('InvalidTransactionDate')
            return

        index2delete = list()
        for transaction in self.transactions:
            if transaction[0] == transaction_date:
                index2delete.append(transaction)
        deleted_transaction_count = len(index2delete)

        if deleted_transaction_count > 1:
            raise NameError('MultipleRemove')
            return

        del self.transactions[self.transactions.index(index2delete[0])]

    def get_transaction(self, transaction_date):
        # Validate the transaction date
        if transaction_date > datetime.date.today():
            raise NameError('InvalidTransactionDate')
            return

        index2return = list()
        for transaction in self.transactions:
            if transaction[0] == transaction_date:
                index2return.append(transaction)
        index_to_return_count = len(index2return)
        if index_to_return_count > 1:
            raise NameError('MultipleGet')
            return

        return self.transactions[self.transactions.index(index2return[0])]

    def get_mean_cost(self):
        pass

    def get_share_nb(self):
        pass

