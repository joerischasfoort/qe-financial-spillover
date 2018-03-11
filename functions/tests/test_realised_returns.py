from numpy.testing import assert_equal, assert_almost_equal
from functions.realised_returns import *
import pytest


@pytest.fixture
def init_params():
    default_probability = 0
    previous_price = 1
    quantity = 1
    face_value = previous_price * quantity
    price = previous_price
    interest_rate = 0.004
    maturity = 1
    return default_probability, previous_price, face_value, quantity, price, interest_rate, maturity

def test_realised_profits_domestic(init_params):
    # if default prob = 0, maturity = 1, P_tau = P, and face_value = P*Q, return is interest rate & m = 1
    default_probability, previous_price, face_value, quantity, price, interest_rate, maturity = init_params
    assert_almost_equal(realised_profits_asset(default_probability, face_value,
                                               previous_price, price, quantity,
                                               interest_rate, maturity), interest_rate, 4)


def test_realised_profits_foreign(init_params):
    default_probability, previous_price, face_value, quantity, price, interest_rate, maturity = init_params
    # with an exchange rate of 1 this should be equal to the previous test
    assert_almost_equal(realised_profits_asset(default_probability, face_value,
                                               previous_price, price, quantity,
                                               interest_rate, maturity, exchange_rate=1,
                                               previous_exchange_rate=1), interest_rate, 4)
