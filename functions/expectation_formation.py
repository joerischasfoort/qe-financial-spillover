from math import log
from math import exp
import numpy as np


def dr_expectations(fund, portfolios, delta_news, fundamental_default_rates, noise):
    """
    Calculate default rate expectations
    :param fund: Fund object for which to calculate default rate expectations
    :param portfolios: Dictionary with portfolio object keys which the fund holds
    :param delta_news: float the difference in the news process about the default rate
    :return: dictionary of assets and corresponding floats of expected default rates
    """
    expected_dr = {}  #TODO: rethink this! Idiosyncratic error terms don't show. Avoid expectations of zero default rate

    for a in portfolios:
        previously_exp_dr = fund.exp.default_rates[a]
        fdr = fundamental_default_rates[a]

        log_exp_dr = log(previously_exp_dr) + delta_news[a] + noise[a] + fund.par.adaptive_param * (
                    log(fdr) - log(previously_exp_dr))
        expected_dr[a] = exp(log_exp_dr)

    return expected_dr


def dr_expectations_oc(fund, portfolios, delta_news, fundamental_default_rates, noise, day):
    """
    Calculate default rate expectations
    :param fund: Fund object for which to calculate default rate expectations
    :param portfolios: Dictionary with portfolio object keys which the fund holds
    :param delta_news: float the difference in the news process about the default rate
    :return: dictionary of assets and corresponding floats of expected default rates
    """
    expected_dr = {}  #TODO: rethink this! Idiosyncratic error terms don't show. Avoid expectations of zero default rate

    for a in portfolios:
        previously_exp_dr = fund.exp.default_rates[a][day - 1]
        fdr = fundamental_default_rates[a]

        log_exp_dr = log(previously_exp_dr) + delta_news[a] + noise[a] + fund.par.adaptive_param * (
                    log(fdr) - log(previously_exp_dr))
        expected_dr[a] = exp(log_exp_dr)

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


def price_expectations(fund, portfolios, day):
    """
    Calculate the price expectations of asset portfolios
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
        realised_dp = asset.var.price[day] / asset.var.price[day - 1]
        ewma_delta_prices[asset] = compute_ewma(realised_dp, fund.var.ewma_delta_prices[asset],
                                                fund.par.price_memory)
        expected_prices[asset] = exp_price_or_fx(asset.var.price[day], asset.var.price[day - 1],
                                                 fund.var.ewma_delta_prices[asset], fund.par.price_memory)

    return ewma_delta_prices, expected_prices


def anchored_FX_expectations(fund, environment, shock):

    exp_fx_anchor = fund.exp.exchange_rate_anchor.copy()
    p_index = {}
    p_index.update({"domestic":0})
    p_index.update({"foreign":0})

    #shocking the domestic price index, which has an impact on the fx anchor
    p_index["domestic"] = environment.par.global_parameters["domestic_price_index"] * (1 + shock)
    p_index["foreign"] = environment.par.global_parameters["foreign_price_index"]

    # updating the expectation of the fx anchor
    for row in fund.exp.exchange_rate_anchor.index:
        for col in fund.exp.exchange_rate_anchor.columns:
            exp_fx_anchor.loc[row, col] = p_index[col] / float(p_index[row])

    exp_exchange_rates = environment.var.fx_rates.copy()
    for c in environment.var.fx_rates:
        if fund.par.country != c:
            fx_reversion_speed = environment.par.global_parameters["fx_reversion_speed"]
            exp_exchange_rates.loc[fund.par.country,c] = environment.var.fx_rates.loc[fund.par.country,c] + (fx_reversion_speed) * ( exp_fx_anchor.loc[fund.par.country,c] - environment.var.fx_rates.loc[fund.par.country,c])

    return exp_exchange_rates, exp_fx_anchor


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
        exp_returns[currency] = ((1+exp_returns[currency] )/(1+fund.exp.inflation[currency.par.country]))-1

    repayment_effect={}
    price_effect={}
    interest_effect={}
    default_effect={}

    for asset in portfolios:
        out = asset.par.maturity * (1 - fund.exp.default_rates[asset])
        mat = (1 - asset.par.maturity) * (1 - fund.exp.default_rates[asset])
        alla = (1 - fund.exp.default_rates[asset])

        repayment_effect[asset] = mat * (
                    fund.exp.exchange_rates.loc[fund.par.country, asset.par.country] * np.divide(asset.par.face_value,
                                                                                                 float(
                                                                                                     asset.par.quantity)) -
                    environment.var.fx_rates.loc[fund.par.country, asset.par.country] * asset.var.price)

        price_effect[asset] = out * (
                    fund.exp.exchange_rates.loc[fund.par.country, asset.par.country] * fund.exp.prices[asset] -
                    environment.var.fx_rates.loc[fund.par.country, asset.par.country] * asset.var.price)

        interest_effect[asset] = alla * fund.exp.exchange_rates.loc[fund.par.country, asset.par.country] * np.divide(
            asset.par.face_value, float(asset.par.quantity)) * asset.par.nominal_interest_rate

        default_effect[asset] = fund.exp.default_rates[asset] * fund.exp.exchange_rates.loc[
            fund.par.country, asset.par.country] * fund.exp.prices[asset]

        exp_returns[asset] = (repayment_effect[asset] + price_effect[asset] + interest_effect[asset] - default_effect[asset])/(asset.var.price* environment.var.fx_rates.loc[fund.par.country][asset.par.country])
        exp_returns[asset] = ((1+exp_returns[asset])/(1+fund.exp.inflation[asset.par.country]))-1

    return exp_returns


def return_expectations_oc(fund, portfolios, currencies, day):
    """
    Calcuate expectated returns on a fund's asset portfolios and currencies, one country model
    :param fund: Fund object for which the returns are calculated
    :param portfolios: Dictionary of Asset objects keys with corresponding values
    :param currencies: Dictionary of Currency objects keys with corresponding values
    :param environment: Environment object which holds a Pandas Dataframe of exchange rates
    :return: Dictionary of portfolio and currency object keys with float return expectations
    """
    exp_returns = {}
    for currency in currencies:
        exp_returns[currency] = currency.par.nominal_interest_rate

    repayment_effect = {}
    price_effect = {}
    interest_effect = {}
    default_effect = {}

    for asset in portfolios:
        out = asset.par.maturity * (1 - fund.exp.default_rates[asset][day])
        mat = (1 - asset.par.maturity) * (1 - fund.exp.default_rates[asset][day])
        alla = (1 - fund.exp.default_rates[asset][day])

        repayment_effect[asset] = mat * (np.divide(asset.par.face_value, float(asset.par.quantity)) - asset.var.price[day])

        price_effect[asset] = out * (fund.exp.prices[asset][day] - asset.var.price[day])

        interest_effect[asset] = alla * np.divide(asset.par.face_value, float(asset.par.quantity)) * asset.par.nominal_interest_rate

        default_effect[asset] = fund.exp.default_rates[asset][day] * fund.exp.prices[asset][day]

        exp_returns[asset] = (repayment_effect[asset] + price_effect[asset] + interest_effect[asset] - default_effect[asset]) / (asset.var.price[day])

    return exp_returns


def covariance_estimate(fund, environment, prev_exp_ret,  inflation_shock):
    """
    Calculate expected weighted moving average of returns and covariance matrix between them
    :param fund: the Fund object for which to make the calculation
    :param portfolios: Dictionary of Asset object keys and quantity values
    :return: dictionary of asset objects and their expected weighted moving average of returns , and
    a pandas DataFrame of covariances of returns between asset portfolios.
    """
    ewma_returns = {}
    realized_returns = {}

    for asset in fund.var.assets:
        # correcting profits with the inflation shock
        key = asset.par.country + "_inflation"


        realized_returns[asset] = fund.var.profits[asset] / (asset.var_previous.price * environment.var_previous.fx_rates.loc[fund.par.country, asset.par.country])
        if asset.par.maturity != 1:
            realized_returns[asset] = ((1 + realized_returns[asset]) / (1 + inflation_shock[key])) - 1




        ewma_returns[asset] = compute_ewma(realized_returns[asset], fund.var_previous.ewma_returns[asset],
                                           environment.par.global_parameters["cov_memory"])

    for cash in fund.var.currency:
        # correcting profits with the inflation shock
        key = cash.par.country + "_inflation"

        realized_returns[cash] = fund.var.profits[cash] / (environment.var_previous.fx_rates.loc[fund.par.country, cash.par.country])
        realized_returns[cash] = ((1 + realized_returns[cash]) / (1 + inflation_shock[key])) - 1


        ewma_returns[cash] = compute_ewma(realized_returns[cash], fund.var_previous.ewma_returns[cash],
                                          environment.par.global_parameters["cov_memory"])

    new_covariance_matrix = fund.var.covariance_matrix.copy()
    new_correlation_matrix = fund.var.covariance_matrix.copy()
    old_correlation_matrix = fund.var_previous.covariance_matrix.copy()
    for idx_x, asset_x in enumerate(new_covariance_matrix.columns):
        for idx_y, asset_y in enumerate(new_covariance_matrix.columns):
           if idx_x <= idx_y:
                covar = (realized_returns[asset_x] - ewma_returns[asset_x]) * (realized_returns[asset_y] - ewma_returns[asset_y])

                ewma_covar = compute_ewma(covar, fund.var_previous.covariance_matrix.loc[asset_x][asset_y], environment.par.global_parameters["cov_memory"])
                new_covariance_matrix.loc[asset_x][asset_y] = ewma_covar
                new_covariance_matrix.loc[asset_y][asset_x] = ewma_covar

    for idx_x, asset_x in enumerate(new_covariance_matrix.columns):
        for idx_y, asset_y in enumerate(new_covariance_matrix.columns):
            if idx_x <= idx_y:
                new_correlation_matrix.loc[asset_x][asset_y] =(new_covariance_matrix.loc[asset_y][asset_x] / (np.sqrt(new_covariance_matrix.loc[asset_y][asset_y]) * np.sqrt(new_covariance_matrix.loc[asset_x][asset_x])))*100
                new_correlation_matrix.loc[asset_y][asset_x] = new_correlation_matrix.loc[asset_x][asset_y]
                old_correlation_matrix.loc[asset_x][asset_y] = (fund.var_previous.covariance_matrix.loc[asset_y][asset_x] / (np.sqrt(fund.var_previous.covariance_matrix.loc[asset_y][asset_y]) * np.sqrt(fund.var_previous.covariance_matrix.loc[asset_x][asset_x])))*100
                old_correlation_matrix.loc[asset_y][asset_x] = old_correlation_matrix.loc[asset_x][asset_y]

    for x in new_covariance_matrix.index:
        for y in new_covariance_matrix.columns:
            new_covariance_matrix.loc[x,y] = max(0,new_covariance_matrix.loc[x,y])

    return ewma_returns, new_covariance_matrix, realized_returns


def covariance_estimate_oc(fund, parameters, day):
    """
    Calculate expected weighted moving average of returns and covariance matrix between them
    :param fund: the Fund object for which to make the calculation
    :param portfolios: Dictionary of Asset object keys and quantity values
    :return: dictionary of asset objects and their expected weighted moving average of returns , and
    a pandas DataFrame of covariances of returns between asset portfolios.
    """
    ewma_returns = {}
    realized_returns = {}

    for asset in fund.var.assets:
        realized_returns[asset] = fund.var.profits[asset][day] / (asset.var.price[day - 1])
        ewma_returns[asset] = compute_ewma(realized_returns[asset], fund.var.ewma_returns[asset][day - 1], parameters["cov_memory"])

    for c in fund.var.currency:
        realized_returns[c] = fund.var.profits[c][day]
        ewma_returns[c] = compute_ewma(fund.var.profits[c][day], fund.var.ewma_returns[c][day - 1], parameters["cov_memory"])
        #TODO add realized returns c

    new_covariance_matrix = fund.var.covariance_matrix[day].copy()
    new_correlation_matrix = fund.var.covariance_matrix[day].copy()
    old_correlation_matrix = fund.var.covariance_matrix[day - 1].copy()
    for idx_x, asset_x in enumerate(new_covariance_matrix.columns):
        for idx_y, asset_y in enumerate(new_covariance_matrix.columns):
            if idx_x <= idx_y:
                covar = (realized_returns[asset_x] - ewma_returns[asset_x]) * (realized_returns[asset_y] - ewma_returns[asset_y])

                ewma_covar = compute_ewma(covar, fund.var.covariance_matrix[day - 1].loc[asset_x][asset_y], parameters["cov_memory"])
                new_covariance_matrix.loc[asset_x][asset_y] = ewma_covar
                new_covariance_matrix.loc[asset_y][asset_x] = ewma_covar

    for idx_x, asset_x in enumerate(new_covariance_matrix.columns):
        for idx_y, asset_y in enumerate(new_covariance_matrix.columns):
            if idx_x <= idx_y:
                new_correlation_matrix.loc[asset_x][asset_y] = (new_covariance_matrix.loc[asset_y][asset_x] / (np.sqrt(new_covariance_matrix.loc[asset_y][asset_y]) * np.sqrt(new_covariance_matrix.loc[asset_x][asset_x])))*100
                new_correlation_matrix.loc[asset_y][asset_x] = new_correlation_matrix.loc[asset_x][asset_y]
                old_correlation_matrix.loc[asset_x][asset_y] = (fund.var.covariance_matrix[day - 1].loc[asset_y][asset_x] / (np.sqrt(fund.var.covariance_matrix[day - 1].loc[asset_y][asset_y]) * np.sqrt(fund.var.covariance_matrix[day - 1].loc[asset_x][asset_x])))*100
                old_correlation_matrix.loc[asset_y][asset_x] = old_correlation_matrix.loc[asset_x][asset_y]

    for x in new_covariance_matrix.index:
        for y in new_covariance_matrix.columns:
            new_covariance_matrix.loc[x, y] = max(0, new_covariance_matrix.loc[x, y])

    return ewma_returns, new_covariance_matrix, realized_returns


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
