from numpy.testing import assert_equal, assert_almost_equal
from functions.realised_returns import *
from init_objects import *
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


@pytest.fixture
def params():
    """Returns global parameter which indicates there are four assets"""
    # 1 setup parameters
    parameters = {
        # global parameters
        "n_domestic_assets": 2,
        "n_foreign_assets": 3,
        "n_domestic_funds": 3,
        "n_foreign_funds": 2,
        "days": 10,
        "p_change_intensity": 0.1,
        "fx_change_intensity": 0.1,
        # asset parameters
        "face_value": 5000,
        "default_rate": 0.012,
        "nominal_interest_rate": 0.003,
        "currency_rate": 0,
        "maturity": 0.99,
        "quantity": 5000,
        # agent parameters
        "price_memory": 0.6,
        "fx_memory": 0.6,
        "risk_aversion": 1,
        "news_evaluation_error": 0.001,
        "fund_target_growth": 0.0,
        # cb parameters
        "cb_country": 'domestic',
        # initial values
        "init_asset_price": 1,
        "init_exchange_rate": 1,
        "total_money": 4000,
        "init_agent_ewma_delta_prices": 0,
        "init_ewma_delta_fx": 0,
        "init_asset_demand": 0,
        "init_currency_demand": 0,
        "init_payouts": 0,
        "init_profits": 0,
        # shock processes parameters
        "fx_shock_mu": 0.0,
        "fx_shock_std": 0.001,
        "default_rate_mu": 10e-7,
        "default_rate_std": 0.125,
        "default_rate_mean_reversion": 0.99,
        "default_rate_delta_t": 0.003968253968253968,
        "adaptive_param": 0.5
    }
    return parameters


def test_hypothetical_asset_returns(params):
    portfolios, currencies, funds, environment, exogeneous_agents = init_objects(params)
    prices_tau = {portfolio: portfolio.var.price for portfolio in portfolios}
    assert_equal(len(hypothetical_asset_returns(funds[0], prices_tau, environment.var.fx_rates)[0]), 5)
    # TODO right more rigorous logical tests


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
