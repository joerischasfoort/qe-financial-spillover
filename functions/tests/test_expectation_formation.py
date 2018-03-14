from numpy.testing import assert_equal
from functions.expectation_formation import *
from init_objects import *
from tests.test_init_objects import parameters
import pytest


def test_exp_return_asset(parameters):
    """Test the expected retrun on asset function"""
    portfolios, currencies, funds, environment, exogeneous_agents = init_objects(parameters)
    exp_return_asset(portfolios[0], funds[0], environment.var.fx_rates)


def test_exp_default_probability(parameters):
    """Test if the expectations about default probability are formed correctly"""
    portfolios, currencies, funds, environment, exogeneous_agents = init_objects(parameters)
    # if the actual default rate was bigger than previous expectations the next expectation will be higher
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


def test_exp_return_cash(parameters):
    """Test if the return on foreign and home country cash is correctly calculated"""
    portfolios, currencies, funds, environment, exogeneous_agents = init_objects(parameters)
    # the return on cash from the home country should be equal to the interest rate
    assert_equal(exp_return_cash(funds[0], currencies[0], environment.var.fx_rates),
                 currencies[0].par.nominal_interest_rate)
    # return on cash from a foreign country should not be equal to the interest rate
    #assert_equal(exp_return_cash(fund1, currency2, fx_matrix) != currency2.par.nominal_interest_rate, True)
    # TODO test direction


def test_update_expectations(parameters):
    portfolios, currencies, funds, environment, exogeneous_agents = init_objects(parameters)
    prices_tau = {portfolio: 1.01 for portfolio in portfolios}
    delta_news = 2
    #print(update_expectations(funds[0], environment, prices_tau, delta_news))


#test_exp_return_cash(params())
#test_update_expectations(params())