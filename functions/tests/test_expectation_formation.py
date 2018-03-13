from numpy.testing import assert_equal
from functions.expectation_formation import *
from init_objects import *
import pytest


@pytest.fixture
def params():
    """Returns global parameter which indicates there are four assets"""
    # 1 setup parameters
    parameters = {
        # global parameters
        "n_domestic_assets": 1,
        "n_foreign_assets": 1,
        "n_domestic_funds": 1,
        "n_foreign_funds": 1,
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


def test_exp_default_probability(params):
    """Test if the expectations about default probability are formed correctly"""
    portfolios, currencies, funds, environment, exogeneous_agents = init_objects(params)
    # if the actual default rate was bigger than previous expectations the next expecation will be higher
    previous_expectation = 0.0007
    funds[0].exp.default_rates[portfolios[0]] = previous_expectation
    portfolios[0].var.default_rate = 0.001
    assert_equal(exp_default_rate(funds[0], portfolios[0], delta_news=0, std_noise=0) > previous_expectation, True)
    # if the default rate was equal to expectations but the news process is positive (higher likelyhood of default)
    # the default probability will go up
    previous_expectation = 0.001
    funds[0].exp.default_rates[portfolios[0]] = previous_expectation
    assert_equal(exp_default_rate(funds[0], portfolios[0], delta_news=2, std_noise=0) > previous_expectation, True)


def test_compute_ewma():
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


def test_exp_return_cash(params):
    """Test if the return on foreign and home country cash is correctly calculated"""
    portfolios, currencies, funds, environment, exogeneous_agents = init_objects(params)
    # the return on cash from the home country should be equal to the interest rate
    assert_equal(exp_return_cash(funds[0], currencies[0], environment.var.fx_rates),
                 currencies[0].par.nominal_interest_rate)
    # return on cash from a foreign country should not be equal to the interest rate
    #assert_equal(exp_return_cash(fund1, currency2, fx_matrix) != currency2.par.nominal_interest_rate, True)
    # TODO test direction


def test_update_expectations(params):
    portfolios, currencies, funds, environment, exogeneous_agents = init_objects(params)
    prices_tau = {portfolio: 1.01 for portfolio in portfolios}
    delta_news = 2
    #print(update_expectations(funds[0], environment, prices_tau, delta_news))


#test_exp_return_cash(params())
#test_update_expectations(params())