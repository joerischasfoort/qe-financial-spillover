from init_objects import *
from objects.modelparameters import *
from numpy.testing import assert_equal
import pytest

@pytest.fixture
def parameters():
    """Returns global parameter which indicates there are four assets"""
    parameters = {
        # global parameters
        "n_assets": 4,
        "n_funds": 2,
        "days": 10,
        "regions": ['domestic', 'foreign'],
        "p_change_intensity": 0.1,
        # asset parameters
        "face_value": 100,
        "default_rate": 0.012,
        "nominal_interest_rate": 0.003,
        "cash_return": 0,
        "maturity": 1,
        "quantity": 5000,
        # agent parameters
        "price_memory": 2,
        "fx_memory": 2,
        "risk_aversion": 1,
        # initial values
        "init_asset_price": 1,
        "init_exchange_rate": 1,
        "total_money": 4000
    }
    return parameters


def test_init_objects(parameters):
    assets, funds = init_objects(parameters)
    # test 1 the function creates four assets and two funds
    assert_equal(len(assets), 4)
    assert_equal(len(funds), 2)
    # test 2 funds assets = liabilities
    sum_portfolio_values = 0
    total_money = 0
    for fund in funds:
        assert_equal(fund.var.money + sum(fund.var.assets.values()) == fund.var.redeemable_shares, True)
        sum_portfolio_values += sum(fund.var.assets.values())
        total_money += fund.var.money
    # test 3 sum of fund portfolio values = global portfolio values
    assert_equal(sum_portfolio_values, (parameters["quantity"] * len(assets)))
    # test 4 sum of money held by funds is global money input
    assert_equal(total_money, parameters["total_money"])

test_init_objects(parameters())