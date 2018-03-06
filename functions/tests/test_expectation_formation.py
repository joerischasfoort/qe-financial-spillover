from numpy.testing import assert_equal
from functions.expectation_formation import *
from functions.supercopy import *
from objects.fund import *
from objects.asset import *
import pytest
import pandas as pd


@pytest.fixture
def funds_and_assets():
    portfolios = []
    asset_nationalities = ['domestic', 'foreign']
    for idx in range(2):
        asset_params = AssetParameters(asset_nationalities[idx], 100, 0.002, 0.99, 500)
        init_asset_vars = AssetVariables(1, 0.001)
        previous_assets_vars = AssetVariables(1, 0.0005)
        portfolios.append(Asset(idx, init_asset_vars, previous_assets_vars, asset_params))

    obj1, obj2 = portfolios[0], portfolios[1]
    funds = []
    fund_nationalities = ['domestic', 'foreign']
    for idx in range(2):
        fund_vars = AgentVariables(assets={obj1: 20, obj2: 30}, currency={'currency1': 20},
                               redeemable_shares=10, asset_demand={obj1: 1, obj2: 2},
                               currency_demand={'currency1': 2}, ewma_returns={obj1: 2, obj2: 3},
                               ewma_delta_prices={obj1: 2, obj2: 3},
                               ewma_delta_fx={'currency1': 2},
                               covariance_matrix=pd.DataFrame({obj1: [1, 2], obj2: [0, 2]}),
                               payouts={obj1: 2, obj2: 2}, weights={obj1: 2, obj2: 3})
        fund_params = AgentParameters(fund_nationalities[idx], 2, 2, 1, 0.5)
        fund_expectations = AgentExpectations({obj1: 0.003, obj2: 0.002}, {obj1: 0.0007, obj2: 0.001}, 1, 0)
        funds.append(Fund(idx, fund_vars, copy_agent_variables(fund_vars), fund_params, fund_expectations))
    return funds, obj1, obj2



def test_exp_default_probability(funds_and_assets):
    fund1, fund2 = funds_and_assets[0]
    asset0, asset1 = funds_and_assets[1], funds_and_assets[1]
    # if the actual default rate was bigger than previous expectations the next expecation will be higher
    previous_value = 0.0007
    fund1.exp.default_rates[asset0] = previous_value
    asset0.var.default_rate = 0.001
    assert_equal(exp_default_rate(fund1, asset0, delta_news=0, std_noise=0)> previous_value, True)

test_exp_default_probability(funds_and_assets())