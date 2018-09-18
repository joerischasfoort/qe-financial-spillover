
from math import log
from math import exp
import numpy as np
import pandas as pd


def dr_expectations(fund, portfolios, delta_news, fundamental_default_rates, noise):
    """
    Calculate default rate expectations
    :param fund: Fund object for which to calculate default rate expectations
    :param portfolios: Dictionary with portfolio object keys which the fund holds
    :param delta_news: float the difference in the news process about the default rate
    :return: dictionary of assets and corresponding floats of expected default rates
    """
    expected_dr = {} #TODO: rethink this! Idiosyncratic error terms don't show. Avoid expectations of zero default rate

    for a in portfolios:

        previously_exp_dr = fund.exp.default_rates[a]
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


def anchored_FX_expectations(fund, environment, shock):
    """
    Fundals anchor calculation of expected exchange rates
    :param fund: Fund object for which the expectations are calculated
    :param environment: Environment object
    :param shock: float stochastic shock
    :return: expected exchange rates
    """
    exp_fx_anchor = fund.exp.exchange_rate_anchor.copy()
    p_index = {}
    p_index.update({"domestic": 0})
    p_index.update({"foreign": 0})

    # shocking the domestic price index, which has an impact on the fx anchor
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


def heterogeneous_fx_expectations(fund, environment, shock):
    """
    Fx expectations are formed using a trend following and fundamentalist expectations component.
    The anchor or fundamentalist component is the PPP price of the exchange rate.
    :param fund:
    :param environment:
    :param shock:
    :return:
    """
    # 1 Form expectations about the fundamental value / anchor
    exp_fx_anchor = fund.exp.exchange_rate_anchor.copy()
    p_index = {}
    p_index.update({"domestic": 0})
    p_index.update({"foreign": 0})

    # shocking the domestic price index, which has an impact on the fx anchor
    p_index["domestic"] = environment.par.global_parameters["domestic_price_index"] * (1 + shock)
    p_index["foreign"] = environment.par.global_parameters["foreign_price_index"]

    # updating the expectation of the fx anchor
    for row in fund.exp.exchange_rate_anchor.index:
        for col in fund.exp.exchange_rate_anchor.columns:
            exp_fx_anchor.loc[row, col] = p_index[col] / float(p_index[row])

    # updating exchange rate expectations
    exp_exchange_rates = environment.var.fx_rates.copy()

    def sgn(x):
        """Helper function to calculate whether a function would have invested"""
        if x > 1:
            return 1
        elif x == 0:
            return 0
        else:
            return -1

    def fundamentalist_prediction(price, fundamental_price):
        return environment.par.global_parameters["fx_reversion_speed"] * (fundamental_price - price)

    def chartist_prediction(price, weighted_previous_price):
        fx_extrapolation_speed = environment.par.global_parameters["fx_extrapolation_speed"]
        return fx_extrapolation_speed * np.divide(price - weighted_previous_price, weighted_previous_price)

    for c in environment.var.fx_rates:
        if fund.par.country != c:
            change_in_FX = environment.var.fx_rates.loc[fund.par.country,c] - environment.var_previous.fx_rates.loc[fund.par.country,c]

            previous_domestic_indices = {'domestic': p_index["domestic"] / (1 + shock), 'foreign': p_index["foreign"]}
            previous_fundamental_value = previous_domestic_indices[filter(lambda k: c not in k, previous_domestic_indices.keys())[0]] / float(previous_domestic_indices[c]) #TODO check if this works as intended

            fundamentalist_predicted_change = fundamentalist_prediction(environment.var_previous.fx_rates.loc[fund.par.country,c], previous_fundamental_value)
            chartist_predicted_change = chartist_prediction(environment.var_previous.fx_rates.loc[fund.par.country,c], 1) # TODO add previous ewma

            fundamentalist_performance = change_in_FX * sgn(fundamentalist_predicted_change)
            chartist_performance = change_in_FX * sgn(chartist_predicted_change)

            # calculate strategy performance over time
            weight = fund.par.current_strategy_performance_weight
            av_fundamentalist_performance = weight * fundamentalist_performance + (1 - weight) * fund.var.ewma_fundamentalist_performance
            av_chartist_performance = weight * chartist_performance + (1 - weight) * fund.var.ewma_chartist_performance

            # calculate relative attractiveness of fundamentalist strategy over chartist strategy
            strat_performance_w = environment.par.global_parameters["strategy_performance_weight"]
            attractiveness_fundamentalists = strat_performance_w * (av_fundamentalist_performance - av_chartist_performance
                                                                    ) + (1 - strat_performance_w) * (environment.var.fx_rates.loc[fund.par.country,c] - exp_fx_anchor.loc[fund.par.country,c])**2 #TODO check if correct

            # calculate weight of both strategies
            intensity_of_choice = environment.par.global_parameters["intensity_of_choice"]
            weight_fundamentalists = np.divide(1, 1 + np.exp(intensity_of_choice * attractiveness_fundamentalists))
            weight_chartists = 1 - weight_fundamentalists

            # calculate exchange rate expectation
            fundamentalist_prediction = fundamentalist_prediction(environment.var.fx_rates.loc[fund.par.country, c], exp_fx_anchor.loc[fund.par.country,c])
            chartist_prediction = chartist_prediction(environment.var.fx_rates.loc[fund.par.country, c], environment.var_previous.ewma_fx_rates.loc[fund.par.country, c])

            exp_exchange_rates.loc[fund.par.country, c] = weight_fundamentalists * fundamentalist_prediction + weight_chartists * chartist_prediction

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
    exp_cons_returns = {}
    exp_local_currency_returns = {}
    loc_weight=environment.par.global_parameters["local_currency_return_weight"]

    fund_country = fund.par.country

    for currency in currencies:
        exp_local_currency_returns[currency] = (fund.exp.exchange_rates.loc[fund.par.country][currency.par.country] * (
                    1 + currency.par.nominal_interest_rate) - environment.var.fx_rates.loc[fund.par.country][
                                     currency.par.country]) / environment.var.fx_rates.loc[fund.par.country][
                                    currency.par.country]


        currency_country = currency.par.country

        potential_consumption_of_investment = (1)/environment.par.global_parameters[currency_country + "_price_index"]
        potential_consumption_local_currency = environment.var.fx_rates.loc[fund.par.country][currency.par.country]/environment.par.global_parameters[fund_country + "_price_index"]

        exp_cons_returns[currency] = potential_consumption_of_investment/potential_consumption_local_currency -1

        exp_returns[currency] = loc_weight * exp_local_currency_returns[currency] + (1 - loc_weight) * \
                             exp_cons_returns[currency]


    for asset in portfolios:
        out = asset.par.maturity * (1 - fund.exp.default_rates[asset])
        mat = (1 - asset.par.maturity) * (1 - fund.exp.default_rates[asset])
        alla = (1 - fund.exp.default_rates[asset])

        repayment_effect = mat * (
                    fund.exp.exchange_rates.loc[fund.par.country, asset.par.country] * np.divide(asset.par.face_value,
                                                                                                 float(
                                                                                                     asset.par.quantity)) -
                    environment.var.fx_rates.loc[fund.par.country, asset.par.country] * asset.var.price)

        cons_repayment_effect = mat * (np.divide(asset.par.face_value, float(asset.par.quantity)) - asset.var.price)

        price_effect = out * (
                    fund.exp.exchange_rates.loc[fund.par.country, asset.par.country] * fund.exp.prices[asset] -
                    environment.var.fx_rates.loc[fund.par.country, asset.par.country] * asset.var.price)

        cons_price_effect = out * (fund.exp.prices[asset] - asset.var.price)

        interest_effect = alla * fund.exp.exchange_rates.loc[fund.par.country, asset.par.country] * np.divide(
            asset.par.face_value, float(asset.par.quantity)) * asset.par.nominal_interest_rate

        cons_interest_effect = alla * np.divide(asset.par.face_value, float(asset.par.quantity)) * asset.par.nominal_interest_rate

        default_effect = fund.exp.default_rates[asset] * fund.exp.exchange_rates.loc[
            fund.par.country, asset.par.country] * fund.exp.prices[asset]

        cons_default_effect = fund.exp.default_rates[asset] * fund.exp.prices[asset]

        exp_local_currency_returns[asset] = (repayment_effect + price_effect + interest_effect - default_effect) / (
                    environment.var.fx_rates.loc[fund.par.country, asset.par.country] * asset.var.price)

        profit_per_asset_barFX = (cons_repayment_effect + cons_price_effect + cons_interest_effect - cons_default_effect)

        asset_country = asset.par.country

        potential_consumption_of_investment = (asset.var.price + profit_per_asset_barFX)/environment.par.global_parameters[asset_country + "_price_index"]
        potential_consumption_local_currency = (asset.var.price * environment.var.fx_rates.loc[fund.par.country][asset.par.country])/environment.par.global_parameters[fund_country + "_price_index"]


        #exp_cons_returns[asset] = potential_consumption_of_investment/potential_consumption_local_currency -1
        exp_cons_returns[asset] = exp_local_currency_returns[asset]


        exp_returns[asset] = exp_local_currency_returns[asset]

    return exp_local_currency_returns, exp_cons_returns, exp_returns



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
    realized_cons_returns = {}
    realized_local_currency_returns = {}
    fund_country = fund.par.country

    loc_weight=environment.par.global_parameters["local_currency_return_weight"]

    for asset in fund.var.assets:
        # correcting profits with the inflation shock
        key = asset.par.country + "_inflation"


        realized_local_currency_returns[asset] = fund.var.profits[asset] / (asset.var_previous.price * environment.var_previous.fx_rates.loc[fund.par.country, asset.par.country])
        realized_local_currency_returns[asset] = ((1 + realized_local_currency_returns[asset]) / (1 + inflation_shock[key])) - 1

        asset_country = asset.par.country

        possible_consumption_with_investment = (asset.var_previous.price + fund.var.cons_profits[asset]) / \
                                              environment.par.global_parameters[asset_country + "_price_index"]
        possible_consumption_local_currency = (asset.var_previous.price * environment.var_previous.fx_rates.loc[fund.par.country, asset.par.country]) / environment.par.global_parameters[fund_country + "_price_index"]

        #realized_cons_returns[asset] = possible_consumption_with_investment / possible_consumption_local_currency - 1
        #realized_cons_returns[asset] = ((1 + realized_cons_returns[asset]) / (1 + inflation_shock[key])) - 1
        realized_cons_returns[asset]= realized_local_currency_returns[asset]

        realized_returns[asset] = realized_local_currency_returns[asset]





        ewma_returns[asset] = compute_ewma(realized_local_currency_returns[asset], fund.var_previous.ewma_returns[asset],
                                           environment.par.global_parameters["cov_memory"])

    for cash in fund.var.currency:
        # correcting profits with the inflation shock
        key = cash.par.country + "_inflation"

        realized_local_currency_returns[cash] = fund.var.profits[cash] / (environment.var_previous.fx_rates.loc[fund.par.country, cash.par.country])
        realized_local_currency_returns[cash] = ((1 + realized_local_currency_returns[cash]) / (1 + inflation_shock[key])) - 1

        cash_country = cash.par.country

        possible_consumption_with_investment = (1) / \
                                               environment.par.global_parameters[cash_country + "_price_index"]
        possible_consumption_local_currency = (environment.var_previous.fx_rates.loc[
            fund.par.country, cash.par.country]) / environment.par.global_parameters[fund_country + "_price_index"]

        realized_cons_returns[cash] = possible_consumption_with_investment / possible_consumption_local_currency - 1
        realized_cons_returns[cash] = ((1 + realized_cons_returns[cash]) / (1 + inflation_shock[key])) - 1



        realized_returns[cash] = loc_weight*realized_local_currency_returns[cash] + (1-loc_weight)*realized_cons_returns[cash]


        ewma_returns[cash] = compute_ewma(realized_local_currency_returns[cash], fund.var_previous.ewma_returns[cash],
                                          environment.par.global_parameters["cov_memory"])

    new_covariance_matrix = fund.var.covariance_matrix.copy()
    new_correlation_matrix = fund.var.covariance_matrix.copy()
    old_correlation_matrix = fund.var_previous.covariance_matrix.copy()
    for idx_x, asset_x in enumerate(new_covariance_matrix.columns):
        for idx_y, asset_y in enumerate(new_covariance_matrix.columns):
           if idx_x <= idx_y:
                #covar = (realized_local_currency_returns[asset_x] - prev_exp_ret[asset_x]) * (realized_local_currency_returns[asset_y] - prev_exp_ret[asset_y])
                covar = (realized_local_currency_returns[asset_x] - ewma_returns[asset_x]) * (realized_local_currency_returns[asset_y] - ewma_returns[asset_y])

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
