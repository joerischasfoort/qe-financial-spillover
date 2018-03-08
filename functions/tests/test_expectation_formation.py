from numpy.testing import assert_equal
from functions.expectation_formation import *
from functions.supercopy import *
from objects.currency import *
from objects.fund import *
from objects.asset import *
import pytest
import pandas as pd
import numpy as np


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

    # 5 create fx matrix
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

    # 6 create covar matrix
    total_assets = portfolios + currencies
    covs = np.zeros((len(total_assets), len(total_assets)))

    assets = portfolios + currencies
    covariance_matrix = pd.DataFrame(covs, index=assets, columns=assets)

    return funds, obj1, obj2, currencies, fx_matrix, covariance_matrix


def test_exp_default_probability(funds_and_assets):
    """Test if the expectations about default probability are formed correctly"""
    fund1, fund2 = funds_and_assets[0]
    asset0, asset1 = funds_and_assets[1], funds_and_assets[2]
    # if the actual default rate was bigger than previous expectations the next expecation will be higher
    previous_expectation = 0.0007
    fund1.exp.default_rates[asset0] = previous_expectation
    asset0.var.default_rate = 0.001
    assert_equal(exp_default_rate(fund1, asset0, delta_news=0, std_noise=0)> previous_expectation, True)
    # if the default rate was equal to expectations but the news process is positive (higher likelyhood of default)
    # the default probability will go up
    previous_expectation = 0.001
    fund1.exp.default_rates[asset0] = previous_expectation
    assert_equal(exp_default_rate(fund1, asset0, delta_news=2, std_noise=0) > previous_expectation, True)


def test_compute_ewma(funds_and_assets):
    """Test if the ewma function produces a weighted average between actual value & previous ewma"""
    x = 10
    previous_ewma = 11
    assert_equal(compute_ewma(x, previous_ewma, 0.5) < previous_ewma, True)
    assert_equal(compute_ewma(x, previous_ewma, 0.5) > x, True)


def test_compute_covar():
    """Test if the compute covar function produces correct results"""
    x = 10
    previous_ewma_x = 11
    y = 10
    previous_ewma_y = 11
    previous_covar_ewma = 1
    #assert_equal(compute_covar(x, previous_ewma_x, y, previous_ewma_y, previous_covar_ewma, 0.5), True)


def test_exp_return_cash(funds_and_assets):
    """Test if the return on foreign and home country cash is correctly calculated"""
    fund1, fund2 = funds_and_assets[0]
    asset0, asset1 = funds_and_assets[1], funds_and_assets[2]
    currency1, currency2 = funds_and_assets[3]
    fx_matrix = funds_and_assets[4]
    # the return on cash from the home country should be equal to the interest rate
    assert_equal(exp_return_cash(fund1, currency1, fx_matrix), currency1.par.nominal_interest_rate)
    # return on cash from a foreign country should not be equal to the interest rate
    assert_equal(exp_return_cash(fund1, currency2, fx_matrix) != currency2.par.nominal_interest_rate, True)
    # TODO test direction


def test_update_expectations(funds_and_assets):
    fund1, fund2 = funds_and_assets[0]
    asset0, asset1 = funds_and_assets[1], funds_and_assets[2]
    currency1, currency2 = funds_and_assets[3]
    fx_matrix = funds_and_assets[4]
    prices_tau = {asset0: 1.01, asset1: 0.99}
    print(update_expectations(fund1,fx_matrix, prices_tau))


test_update_expectations(funds_and_assets())