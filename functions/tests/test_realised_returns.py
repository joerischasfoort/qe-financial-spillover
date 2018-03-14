from numpy.testing import assert_equal, assert_almost_equal
from functions.realised_returns import *
from init_objects import *
import pytest
from tests.test_init_objects import parameters


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
    """Test realised profit on domestic and foreign assets"""
    default_probability, previous_price, face_value, quantity, price, interest_rate, maturity = init_params
    # 1 test the repayment effect
    # 1.1 for a domestic asset
    maturity = 0
    interest_rate = 0.0
    previous_price = 0.5
    assert_almost_equal(realised_profits_asset(default_probability, face_value,
                                               previous_price, price, quantity,
                                               interest_rate, maturity), 0.5, 2)
    # 1.2 for a foreign asset
    assert_almost_equal(realised_profits_asset(default_probability, face_value,
                                               previous_price, price, quantity,
                                               interest_rate, maturity, exchange_rate=0.5), 0.0, 2)
    # 2 test the price effect
    # 2.1 domestic
    maturity = 1
    assert_almost_equal(realised_profits_asset(default_probability, face_value,
                                               previous_price, price, quantity,
                                               interest_rate, maturity), 0.5, 2)
    # 2.2 foreign
    assert_almost_equal(realised_profits_asset(default_probability, face_value,
                                               previous_price, price, quantity,
                                               interest_rate, maturity, exchange_rate=0.5,
                                               previous_exchange_rate=1.0), 0.0, 2)
    # 3 test the interest rate effect
    # 3.1 if default prob = 0, maturity = 1, P_tau = P, and face_value = P*Q, return is interest rate & m = 1
    default_probability, previous_price, face_value, quantity, price, interest_rate, maturity = init_params
    assert_almost_equal(realised_profits_asset(default_probability, face_value,
                                               previous_price, price, quantity,
                                               interest_rate, maturity), interest_rate, 4)
    # 3.2 with an exchange rate of 1 this should be equal to the previous test
    assert_almost_equal(realised_profits_asset(default_probability, face_value,
                                               previous_price, price, quantity,
                                               interest_rate, maturity, exchange_rate=1,
                                               previous_exchange_rate=1), interest_rate, 4)
    # 4 test the default effect
    interest_rate = 0.0
    default_probability = 0.08
    assert_almost_equal(realised_profits_asset(default_probability, face_value,
                                               previous_price, price, quantity,
                                               interest_rate, maturity), -default_probability, 4)


def test_realised_profits_cash():
    """Test if the function works according to equation 1.3"""
    # for domestic assets the return is equal to the interest rate
    interest_rate = 0.004
    assert_almost_equal(realised_profits_cash(interest_rate, 1.0, 1.0), interest_rate, 4)
    # when the interest rate is zero this still applies
    interest_rate = 0.0
    assert_almost_equal(realised_profits_cash(interest_rate, 1.0, 1.0), interest_rate, 4)
    # also when it is negative
    interest_rate = -0.000001
    assert_almost_equal(realised_profits_cash(interest_rate, 1.0, 1.0), interest_rate, 4)


def test_realised_return_cash():
    """Test realised returns on cash function"""
    interest_rate = 0.0
    assert_almost_equal(realised_return_cash(interest_rate), interest_rate, 3)
    # if the exchange rate is 2 the interest rate should be halved
    interest_rate = 0.04
    assert_almost_equal(realised_return_cash(interest_rate, exchange_rate=2), interest_rate / 2.0, 3)


def test_realised_return():
    """Test realised returns on asset function"""
    realised_profit = 0.04
    price = 2.0
    assert_almost_equal(realised_returns_asset(realised_profit, price, exchange_rate=1), 0.02, 2)
    # if the exchange rate doubles, the returns half
    assert_almost_equal(realised_returns_asset(realised_profit, price, exchange_rate=2), 0.01, 3)


def test_hypothetical_asset_returns(parameters):
    portfolios, currencies, funds, environment, exogeneous_agents = init_objects(parameters)
    prices_tau = {portfolio: portfolio.var.price for portfolio in portfolios}
    assert_equal(len(hypothetical_asset_returns(funds[0], prices_tau, environment.var.fx_rates)[0]), 2)
    assert_equal(type(hypothetical_asset_returns(funds[0], prices_tau, environment.var.fx_rates)[0]), dict)
