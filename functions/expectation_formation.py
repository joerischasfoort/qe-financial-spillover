from math import log
from math import exp
import numpy as np


def dr_expectations(fund, portfolios, delta_news):
    """
    Calculate default rate expectations
    :param fund: Fund object for which to calculate default rate expectations
    :param portfolios: Dictionary with portfolio object keys which the fund holds
    :param delta_news: float the difference in the news process about the default rate
    :return: dictionary of assets and corresponding floats of expected default rates
    """
    expected_dr = {} #TODO: rethink this!
    for portfolio in portfolios:

        previously_exp_dr = fund.exp.default_rates[portfolio]
        default_rate = portfolio.var.default_rate
        noise = np.random.normal(0, fund.par.news_evaluation_error)
        if previously_exp_dr <= 0:
            expected_dr[portfolio] = 0
        else:
            log_exp_dr = log(previously_exp_dr) + delta_news + noise + fund.par.adaptive_param * (
                    log(default_rate) - log(previously_exp_dr))
            expected_dr[portfolio] = exp(log_exp_dr)

    return expected_dr


def price_fx_expectations(fund, portfolios, currencies, environment):
    """
    Calculate the price and exchange rate expectations of currencies and asset portfolios
    :param fund: Fund object for which to calculate expectations
    :param portfolios: Dictionary with portfolio object keys which the fund holds
    :param currencies: Dictionary with currency object keys which the fund holds
    :param environment: Enviornment object which holds a DataFrame of current exchange rates
    :return: Dictionaries of expected weighted moving average delta prices and exchange rates, expected
    prices and exchange rates.
    """
    ewma_delta_prices = {}
    expected_prices = {}
    for asset in portfolios:
        realised_dp = asset.var.price / asset.var_previous.price
        ewma_delta_prices[asset] = compute_ewma(realised_dp, fund.var.ewma_delta_prices[asset],
                                                fund.par.price_memory)
        expected_prices[asset] = exp_price_or_fx(asset.var.price, asset.var_previous.price,
                                                 fund.var.ewma_delta_prices[asset], fund.par.price_memory)

    ewma_delta_fx = {}
    exp_exchange_rates = environment.var.fx_rates.copy()
    for currency in currencies:
        # add delta fx ewma
        current_fx = environment.var.fx_rates.loc[fund.par.country][currency.par.country]
        previous_fx = environment.var_previous.fx_rates.loc[fund.par.country][currency.par.country]
        realised_dfx = current_fx / previous_fx
        ewma_delta_fx[currency] = compute_ewma(realised_dfx, fund.var.ewma_delta_fx[currency],
                                               fund.par.fx_memory)
        # calculate expected fx price
        exp_exchange_rates.loc[fund.par.country][currency.par.country] = exp_price_or_fx(current_fx, previous_fx,
                                                                                         fund.var.ewma_delta_fx[
                                                                                             currency],
                                                                                         fund.par.fx_memory)

    return ewma_delta_prices, ewma_delta_fx, expected_prices, exp_exchange_rates


def return_expectations(fund, portfolios, currencies, environment):
    """
    Calcuate expectated returns on a fund's asset portfolios and currencies
    :param fund: Fund object for which the returns are calculated
    :param portfolios: Dictionary of Asset objects keys with corresponding values
    :param currencies: Dictionary of Currency objects keys with corresponding values
    :param environment: Environment object which holds a Pandas Dataframe of exchange rates
    :return: Dictionary of portfolio and currency object keys with float return expectations
    """
    exp_returns = {}
    for currency in currencies:
        exp_returns[currency] = (fund.exp.exchange_rates.loc[fund.par.country][currency.par.country] * (
                    1 + currency.par.nominal_interest_rate) - environment.var.fx_rates.loc[fund.par.country][
                                     currency.par.country]) / environment.var.fx_rates.loc[fund.par.country][
                                    currency.par.country]

    for asset in portfolios:
        out = asset.par.maturity * (1 - fund.exp.default_rates[asset])
        mat = (1 - asset.par.maturity) * (1 - fund.exp.default_rates[asset])
        alla = (1 - fund.exp.default_rates[asset])

        repayment_effect = mat * (
                    fund.exp.exchange_rates.loc[fund.par.country, asset.par.country] * np.divide(asset.par.face_value,
                                                                                                 float(
                                                                                                     asset.par.quantity)) -
                    environment.var.fx_rates.loc[fund.par.country, asset.par.country] * asset.var.price)
        price_effect = out * (
                    fund.exp.exchange_rates.loc[fund.par.country, asset.par.country] * fund.exp.prices[asset] -
                    environment.var.fx_rates.loc[fund.par.country, asset.par.country] * asset.var.price)
        interest_effect = alla * fund.exp.exchange_rates.loc[fund.par.country, asset.par.country] * np.divide(
            asset.par.face_value, float(asset.par.quantity)) * asset.par.nominal_interest_rate
        default_effect = fund.exp.default_rates[asset] * fund.exp.exchange_rates.loc[
            fund.par.country, asset.par.country] * fund.exp.prices[asset]

        exp_returns[asset] = (repayment_effect + price_effect + interest_effect - default_effect) / (
                    environment.var.fx_rates.loc[fund.par.country, asset.par.country] * asset.var.price)

    return exp_returns


def covariance_estimate(fund, portfolios, environment, currencies):
    """
    Calculate expected weighted moving average of returns and covariance matrix between them
    :param fund: the Fund object for which to make the calculation
    :param portfolios: Dictionary of Asset object keys and quantity values
    :return: dictionary of asset objects and their expected weighted moving average of returns , and
    a pandas DataFrame of covariances of returns between asset portfolios.
    """
    ewma_returns = {}
    hypothetical_returns = {}
    for asset in fund.var.assets:
        hypothetical_returns[asset] = fund.var.profits[asset] / (
                    asset.var_previous.price * environment.var_previous.fx_rates.loc[
                fund.par.country, asset.par.country])
        ewma_returns[asset] = compute_ewma(hypothetical_returns[asset], fund.var_previous.ewma_returns[asset],
                                           environment.par.global_parameters["cov_memory"])

    for cash in fund.var.currency:
        hypothetical_returns[cash] = fund.var.profits[cash] / (
        environment.var_previous.fx_rates.loc[fund.par.country, cash.par.country])
        ewma_returns[cash] = compute_ewma(hypothetical_returns[cash], fund.var_previous.ewma_returns[cash],
                                          environment.par.global_parameters["cov_memory"])

    new_covariance_matrix = fund.var.covariance_matrix.copy()
    for idx_x, asset_x in enumerate(new_covariance_matrix.columns):
        for idx_y, asset_y in enumerate(new_covariance_matrix.columns):
           if idx_x <= idx_y:
                covar = (hypothetical_returns[asset_x] - ewma_returns[asset_x]) * (hypothetical_returns[asset_y] - ewma_returns[asset_y])
                ewma_covar = compute_ewma(covar, fund.var_previous.covariance_matrix.loc[asset_x][asset_y], environment.par.global_parameters["cov_memory"])


                new_covariance_matrix.loc[asset_x][asset_y] = ewma_covar
                new_covariance_matrix.loc[asset_y][asset_x] = ewma_covar



    return ewma_returns, new_covariance_matrix, hypothetical_returns



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
    exp_price = compute_ewma(delta_price, previous_ewma_delta_price, memory_parameter) * current_price
    return exp_price


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
