from init_objects import *
from objects.parameters import *
from numpy.testing import assert_equal
import pytest

@pytest.fixture
def parameters():
    """Returns global parameter which indicates there are four assets"""
    params = Parameters(n_assets=4, n_funds=2, days=10, regions=['domestic', 'foreign'],
                        price_memory=2, fx_memory=2, total_money=4000,
                        face_value=100, default_rate=0.12, repayment_rate=0.3, nominal_interest_rate=0.003, maturity=1,
                        quantity=5000, init_asset_price=1, init_exchange_rate=1)
    return params


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
    assert_equal(sum_portfolio_values, (parameters.quantity * len(assets)))
    # test 4 sum of money held by funds is global money input
    assert_equal(total_money, parameters.total_money)

#test_init_objects(parameters())