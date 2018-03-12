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


def test_realised_profits_assets(init_params):
    # if default prob = 0, maturity = 1, P_tau = P, and face_value = P*Q, return is interest rate & m = 1
    default_probability, previous_price, face_value, quantity, price, interest_rate, maturity = init_params
    assert_almost_equal(realised_profits_asset(default_probability, face_value,
                                               previous_price, price, quantity,
                                               interest_rate, maturity), interest_rate, 4)
    # with an exchange rate of 1 this should be equal to the previous test
    assert_almost_equal(realised_profits_asset(default_probability, face_value,
                                               previous_price, price, quantity,
                                               interest_rate, maturity, exchange_rate=1,
                                               previous_exchange_rate=1), interest_rate, 4)


def test_realised_profits_cash():
    # for domestic assets the return is equal to the interest rate
    interest_rate = 0.004
    assert_almost_equal(realised_profits_cash(interest_rate, 1.0, 1.0), interest_rate, 4)
    # when the interest rate is zero this still applies
    interest_rate = 0.0
    assert_almost_equal(realised_profits_cash(interest_rate, 1.0, 1.0), interest_rate, 4)


def test_realised_return_cash():
    """Test realised returns on cash function"""
    interest_rate = 0.0
    assert_almost_equal(realised_return_cash(interest_rate), interest_rate, 3)
    # if the exchange rate is 2 the interest rate should be halved
    interest_rate = 0.5
    assert_almost_equal(realised_return_cash(interest_rate, exchange_rate=2), interest_rate / 2.0, 3)


def test_realised_return():
    """Test realised returns on asset function"""
    realised_profit = 0.5
    price = 1.0
    assert_almost_equal(realised_returns_asset(realised_profit, price, exchange_rate = 1), 0.5, 3)
    # if the exchange rate doubles, the returns half
    assert_almost_equal(realised_returns_asset(realised_profit, price, exchange_rate=2), 0.25, 3)
