from init_objects import *
from numpy.testing import assert_equal
import pytest

@pytest.fixture
def parameters():
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
        # asset parameters
        "face_value": 100,
        "default_rate": 0.012,
        "nominal_interest_rate": 0.003,
        "currency_rate": 0,
        "maturity": 1,
        "quantity": 5000,
        # agent parameters
        "price_memory": 2,
        "fx_memory": 2,
        "risk_aversion": 1,
        # initial values
        "init_asset_price": 1,
        "init_exchange_rate": 1,
        "total_money": 4000,
        "init_agent_ewma_delta_prices": 0,
        "init_ewma_delta_fx": 0,
        "init_asset_demand": 0,
        "init_currency_demand": 0,
        "init_payouts": 0,
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


def test_init_objects(parameters):
    assets, currencies, funds = init_objects(parameters)
    # test 1 the function creates four assets and two funds
    assert_equal(len(assets), 5)
    assert_equal(len(funds), 5)
    # test 2 funds assets = liabilities
    sum_portfolio_values = 0
    total_money = 0
    for fund in funds:
        assert_equal(sum(fund.var.currency.values()) + sum(fund.var.assets.values()) == fund.var.redeemable_shares, True)
        sum_portfolio_values += sum(fund.var.assets.values())
        total_money += sum(fund.var.currency.values())
    # test 3 sum of fund portfolio values = global portfolio values
    assert_equal(sum_portfolio_values, (parameters["quantity"] * len(assets)))
    # test 4 sum of money held by funds is global money input
    assert_equal(total_money, parameters["total_money"])

#test_init_objects(parameters())