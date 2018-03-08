from numpy.testing import assert_equal
from functions.market_mechanism import *
import pytest

#
import pandas as pd
import numpy as np


#To create objects we will test with
from objects.currency import *
from objects.fund import *
from objects.asset import *


# Like in tests_expectation formation
def funds_and_assets():
    portfolios = []
    asset_nationalities = ['domestic', 'foreign']
    
    for idx in range(2):                                                                #          country
                                                                                                #   face_value
                                                                                                #   nominal_interest_rate
                                                                                                #  maturity
                                                                                                # quantity
        asset_params = AssetParameters(asset_nationalities[idx], 100, 0.002, 0.99, 500)  #  AssetParameters(asset_nationalities[idx], 100, 0.002, 0.99, 500)
        init_asset_vars = AssetVariables(1, 0.001)  #   price, default_rate 
        previous_assets_vars = AssetVariables(1, 0.0005)  # price, default_rate 
        portfolios.append(Asset(idx, init_asset_vars, previous_assets_vars, asset_params))

    obj1, obj2 = portfolios[0], portfolios[1]

    currencies = []
    total_currency = 2000
    
    for idx, country in enumerate(set(asset_nationalities)):
        currency_param = CurrencyParameters(country, 0.0,
                                            np.divide(total_currency, len(set(asset_nationalities))))
        currencies.append(Currency(idx, currency_param))

    funds = []
    fund_nationalities = ['domestic', 'foreign']
    for idx in range(2):
        fund_vars = AgentVariables(assets={obj1: 20, obj2: 30}, currency={currencies[0]: 20, currencies[1]: 20},
                               redeemable_shares=10, asset_demand={obj1: 1, obj2: 2},
                               currency_demand={currencies[0]: 2, currencies[1]: 3}, ewma_returns={obj1: 2, obj2: 3},
                               ewma_delta_prices={obj1: 2, obj2: 3},
                               ewma_delta_fx={currencies[0]: 2, currencies[0]: 2},
                               covariance_matrix=pd.DataFrame({obj1: [1, 2], obj2: [0, 2]}),
                               payouts={obj1: 2, obj2: 2}, weights={obj1: 2, obj2: 3})
        
        fund_params = AgentParameters(fund_nationalities[idx], 2, 2, 1, 0.5)
        fund_expectations = AgentExpectations({obj1: 0.003, obj2: 0.002}, {obj1: 0.0007, obj2: 0.001},
                                              {currencies[0]: 1, currencies[1]:1}, {obj1: 1.0, obj2: 1.0}, 0)
        funds.append(Fund(idx, fund_vars, copy_agent_variables(fund_vars), fund_params, fund_expectations))

    # 5 create environment with exchange rates
    fx_matrix = np.zeros([len(currencies), len(currencies)])
    fx_matrix = pd.DataFrame(fx_matrix, index=currencies, columns=currencies)

    for c1, c2 in zip(currencies, currencies[::-1]):
        fx = 0.8
        if c1.par.country == 'foreign':
            fx = 1 / fx
        fx_matrix.loc[c1, c2] = fx
        fx_matrix.loc[c1, c1] = 1

    currency_countries = {c: c.par.country for c in currencies}
    fx_matrix.rename(index=currency_countries, inplace=True)
    fx_matrix.rename(columns=currency_countries, inplace=True)

    return funds, obj1, obj2, currencies, fx_matrix

@pytest.fixture
def set_of_funds():
    """Creates a set of simple funds where the market clears at p=1"""
    class Fund():
        def __init__(self, price_belief):
            self.price_belief = price_belief

        def get_demand(self, price, asset):
            # demand is a function of the price
            demand = (self.price_belief - price) * 100
            return int(demand)

    return [Fund(p) for p in (0.7, 0.8, 0.9, 1.1, 1.2, 1.3)]

@pytest.fixture
def asset():
    class Asset():
        def __init__(self, global_quantity):
            self.parameters = {"global_quantity": global_quantity}

    return Asset(global_quantity=500)


def price_adjustment(portfolios, currencies, environment, exogeneous_agents , funds, asset_object):
    
    
    
    


def test_incomplete_walrasian_auction_price_clears(set_of_funds, asset):
    """Test if the market clears at price 1 and does not clear at other prices"""
    # asset = asset
    # std_market_noise = 0.001
    # imperfection_tolerance = 10
    # price_step = 0.10
    # funds = set_of_funds
    # previous_price = 1
    # assert_equal(incomplete_walrasian_auction_price(asset, funds, previous_price,
    #                                                 imperfection_tolerance,
    #                                                 price_step, std_market_noise)[0], True)
    # previous_price = 0.7
    # assert_equal(incomplete_walrasian_auction_price(asset, funds, previous_price,
    #                                                 imperfection_tolerance,
    #                                                 price_step, std_market_noise)[0], False)
    # previous_price = 1.4
    # assert_equal(incomplete_walrasian_auction_price(asset, funds, previous_price,
    #                                                 imperfection_tolerance,
    #                                                 price_step, std_market_noise)[0], False)
    pass



def test_incomplete_walrasian_auction_price_clears(set_of_funds, asset):
    """Test if the market clears at price 1 and does not clear at other prices"""
    # asset = asset
    # std_market_noise = 0.001
    # imperfection_tolerance = 10
    # price_step = 0.10
    # funds = set_of_funds
    # previous_price = 1
    # assert_equal(incomplete_walrasian_auction_price(asset, funds, previous_price,
    #                                                 imperfection_tolerance,
    #                                                 price_step, std_market_noise)[0], True)
    # previous_price = 0.7
    # assert_equal(incomplete_walrasian_auction_price(asset, funds, previous_price,
    #                                                 imperfection_tolerance,
    #                                                 price_step, std_market_noise)[0], False)
    # previous_price = 1.4
    # assert_equal(incomplete_walrasian_auction_price(asset, funds, previous_price,
    #                                                 imperfection_tolerance,
    #                                                 price_step, std_market_noise)[0], False)
    pass


 

