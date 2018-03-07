from math import log
from math import exp
from functions.realised_returns import *


def update_expectations():
    """
    Method to update expected asset attributes for the next iteration
    1) New expected default probability Equation 1.6
    2) New expected prices, exchange rates Equation 1.7
    3) New expected returns Equation 1.1
    4) Get realised returns for covariance variance matrix  Equation 1.3
    5) Compute new ewma (Mhat) for realised returns   Equation 1.5
    6) Use latest realised
    return and ewma mhat for covariance   Equation 1.4
    5) Calculate new ewma covariance Equation 1.3 continued
    """

    pass


def exp_return_asset(asset, fund, fx_matrix):
    """
    Equation 1.5 - 1.6 Method to calculate the expected returns of assets which go into portfolio optimisation
    :param asset: object Asset over which the return is calculated
    :param fund: object Fund which makes the calculation
    :param fx_matrix: pandas DataFrame containing exchange rates
    :return: float expected return for that asset
    """
    exp_return = (1 - fund.exp.default_rates[asset]) * (
            ((fund.exp.exchange_rate[asset] * asset.par.face_value) / (
                    fx_matrix.loc[fund.par.country][asset.par.country] * asset.var.price * fund.var.assets[asset])
             ) * (asset.par.nominal_interest_rate + 1 - asset.par.maturity) +
            ((asset.par.maturity * fund.exp.exchange_rates[asset] * fund.exp.prices[asset] / (
                    fx_matrix.loc[fund.par.country][asset.par.country] * asset.var.price)
              ) - 1) - fund.exp.default_rates[asset])
    return exp_return


def exp_return_cash(fund, currency, fx_matrix):
    """
    Equation 1.7 Expected return on a currency
    :param fund: object Fund for which the expected return on cash is calculated
    :param currency: object Currency about which the expected return is formed
    :param fx_matrix: pandas DataFrame which contains current exchange rates
    :return: float expected return on currency of interest
    """
    expected_return = currency.par.nominal_interest_rate + (
            fund.exp.exchange_rates[currency] / fx_matrix.loc[fund.par.country][currency.par.country] - 1)
    return expected_return


def compute_covar(x, previous_ewma_x, y, previous_ewma_y, previous_covar, memory_parameter):
    """
    Equation 1.8 Compute covariance between x and y
    :param x: float first variable
    :param previous_ewma_x: float previous exponentially weighted average of x
    :param y: float second variable
    :param previous_ewma_y: float previous exponentially weighted average of y
    :param previous_covar: float previous ewma covariance
    :param memory_parameter: float agent memory paraemter
    :return: float new expected weighted moving average covariance between x and y
    """
    covar = (x - compute_ewma(x, previous_ewma_x, memory_parameter)) * (y - compute_ewma(y, previous_ewma_y, memory_parameter))
    ewma_covar = compute_ewma(covar , previous_covar, memory_parameter)
    return ewma_covar


def compute_ewma(variable, previous_ewma, memory_parameter):
    """
    Equation 1.9 For a fund, calculate expected weighted moving average
    :param variable: float variable of interest
    :param previous_ewma: float previous exponentially weighted moving average
    :param memory_parameter: float the
    :return: estimate of the exponentially weighted moving average of the variable
    """
    ewma = (1 - memory_parameter) * previous_ewma + memory_parameter * variable
    return ewma


def exp_default_rate(fund, asset, delta_news, std_noise):
    """
    Equation 1.10 For a fund, calculate the expected default rate of a certain asset
    :param fund: Fund object which formes the expectation
    :param asset: Asset object about which the expectation is formed
    :param delta_news: float change in the news process about the asset
    :param std_noise: float standard deviation of the agent uncertainty about the news process
    :return: float of the expected default rate
    """
    previously_exp_dr = fund.exp.default_rates[asset]
    default_rate = asset.var.default_rate
    noise = np.random.normal(0, std_noise)
    log_exp_default_rate = log(previously_exp_dr) + delta_news + noise + fund.par.adaptive_param * (log(default_rate) - log(previously_exp_dr))
    exp_default_rate = exp(log_exp_default_rate)
    return exp_default_rate


def exp_price_or_fx(current_price, previous_price, previous_ewma_delta_price, memory_parameter):
    """
    Equation 1.11 calculate expected price or exchange rate
    :param current_price: float current price or exchange rate
    :param previous_price: float previous price or exchange rate
    :param previous_ewma_delta_price: float previous exponentially weighted moving average of delta price
    :param memory_parameter: float agent memory
    :return: float of the expected price or exchange rate
    """
    delta_price = current_price / previous_price
    exp_price = compute_ewma(delta_price, previous_ewma_delta_price, memory_parameter) * previous_price
    return exp_price
