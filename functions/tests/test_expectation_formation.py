from numpy.testing import assert_equal
from functions.expectation_formation import *
from functions.supercopy import *
from objects.fund import *
from objects.asset import *
import pytest
import pandas as pd

@pytest.fixture
def assets():
    portfolios = []
    asset_nationalities = ['domestic', 'foreign']
    for idx in range(2):
        asset_params = AssetParameters(asset_nationalities[idx], 100, 0.002, 0.99, 500)
        init_asset_vars = AssetVariables(1, 0.001)
        previous_assets_vars = AssetVariables(1, 0.0005)
        portfolios.append(Asset(idx, init_asset_vars, previous_assets_vars, asset_params))
    return portfolios[0], portfolios[1]


@pytest.fixture
def funds(assets):
    obj1, obj2 = assets
    funds = []
    fund_nationalities = ['domestic', 'foreign']
    for idx in range(2):
        fund_vars = AgentVariables(assets={obj1: 20, obj2: 30}, currency={'currency1': 20},
                               redeemable_shares=10, asset_demand={obj1: 1, obj2: 2},
                               currency_demand={'currency1': 2}, ewma_returns={obj1: 2, obj2: 3},
                               ewma_delta_prices={obj1: 2, obj2: 3},
                               ewma_delta_fx={'currency1': 2},
                               covariance_matrix=pd.DataFrame({obj1: [1, 2], obj2: [0, 2]}),
                               payouts={obj1: 2, obj2: 2}, weights={obj1: 2, obj2: 3},
                               asset_xfx={obj1: 0, obj2: 1})
        fund_params = AgentParameters(fund_nationalities[idx], 2, 2, 1, 0.5)
        fund_expectations = AgentExpectations({obj1: 0.003, obj2: 0.002}, {obj1: 0.0007, obj2: 0.001}, 1, 0)
        funds.append(Fund(idx, fund_vars, copy_agent_variables(fund_vars), fund_params, fund_expectations))
    return funds


def test_exp_default_probability():
    pass

#print(funds(assets()))