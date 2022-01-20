import pytest
import pandas as pd

from finance.transactions_utils import validate_transactions


def test_validate_transactions():
    transations = [{"Date": "2012-05-16", "Price": "33.36", "Quantity": "100"},
                   {"Date": "2014-07-13", "Price": "20.06", "Quantity": "50"}]
    transactions_df = pd.DataFrame(transations)
    transactions_df["Date"] = pd.to_datetime(transactions_df["Date"]).dt.date

    validation_result = validate_transactions(transactions_df)

    assert validation_result is True, pytest.fail("Test failed")
