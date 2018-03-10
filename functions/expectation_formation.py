from math import log
from math import exp
from functions.realised_returns import *


def update_expectations(fund, environment, prices_tau, delta_news):
    """
    Method to update expected asset attributes for the next iteration
    The agent forms its expectations about:
    1) Calculate hypothetical realised returns?
    2) Calculate ewma's
    3) Calculate covariance realised returns
    4) Calculate expected default probability
    5) Calculate Expected Price
    6) Calculate Expected Exchange rate
    7) Calculate expected return on cash
    8) Calculate expected returns on assets
    """
    # 1 calculate hypothetical realised returns vis a vis previous turn
    realised_rets = {}
    for asset in fund.var.assets:
        realised_rets[asset] = realised_returns(asset.var.default_rate,
                                                asset.par.face_value,
                                                asset.var.price,
                                                prices_tau[asset],
                                                fund.var.assets[asset],
                                                asset.par.nominal_interest_rate,
                                                asset.par.maturity,
                                                environment.var.fx_rates.loc[fund.par.country][asset.par.country])

        # 2 calcultate ewmas
        fund.var.ewma_returns[asset] = compute_ewma(realised_rets[asset], fund.var.ewma_returns[asset], fund.par.price_memory)
        realised_dp = asset.var.price - asset.var_previous.price
        fund.var.ewma_delta_prices[asset] = compute_ewma(realised_dp, fund.var.ewma_delta_prices[asset], fund.par.price_memory)

    # 3 calculate covariance realised returns
    for asset_x, asset_y in zip(list(fund.var.assets), list(fund.var.assets)[::-1]):
        fund.var.covariance_matrix.loc[asset_x][asset_y] = compute_covar(realised_rets[asset_x],
                                                                       fund.var.ewma_returns[asset_x],
                                                                       realised_rets[asset_y],
                                                                       fund.var.ewma_returns[asset_y],
                                                                       fund.var.covariance_matrix.loc[asset_x][asset_y],
                                                                       fund.par.price_memory)

    # 4 Calculate expected default probability & price
    for asset in fund.var.assets:
        fund.exp.default_rates[asset] = exp_default_rate(fund, asset, delta_news,
                                                         environment.par.global_parameters["news_evaluation_error"])
        fund.exp.prices[asset] = exp_price_or_fx(asset.var.price, asset.var_previous.price,
                                                 fund.var.ewma_delta_prices[asset], fund.par.price_memory)

    for currency in fund.var.currency:
        # add delta fx ewma
        current_fx = environment.var.fx_rates.loc[fund.par.country][currency.par.country]
        previous_fx = environment.var_previous.fx_rates.loc[fund.par.country][currency.par.country]
        realised_dfx =current_fx - previous_fx
        fund.var.ewma_delta_fx[currency] = compute_ewma(realised_dfx, fund.var.ewma_delta_fx[currency],
                                                        fund.par.fx_memory)
        # calculate expected fx price
        fund.exp.exchange_rates[currency] = exp_price_or_fx(current_fx, previous_fx,
                                                            fund.var.ewma_delta_fx[currency], fund.par.fx_memory)
        # calculate expected return on fx??
        fund.exp.cash_returns[currency] = 2


def hypothetical_returns():
    """Calculate hypothetical returns on asset portfolio"""
    pass


def asset_ewma(fund):
    """
    Update exponentially weighted moving average on asset delta prices and returns
    :param fund: object Fund for which to calculate asset ewma
    :return: dictionaries of ewma returns and delta prices for every asset
    """
    ewma_returns = {}
    ewma_delta_prices = {}
    for asset in fund.var.assets:
        ewma_returns[asset] = compute_ewma(fund.var.realised_returns[asset], fund.var.ewma_returns[asset],
                                                    fund.par.price_memory)
        realised_dp = asset.var.price - asset.var_previous.price
        ewma_delta_prices[asset] = compute_ewma(realised_dp, fund.var.ewma_delta_prices[asset],
                                                         fund.par.price_memory)
    return ewma_returns, ewma_delta_prices

def asset_covariances(fund):
    """
    Update covariance matrix of assets
    :param fund: object Fund for which to calculate new covariance matrix
    :return: pandas DataFrame of coriance between asset returns
    """
    new_covariance_matrix = fund.var.covariance_matrix.copy()
    for asset_x, asset_y in zip(list(fund.var.assets), list(fund.var.assets)[::-1]):
        new_covariance_matrix.loc[asset_x][asset_y] = compute_covar(fund.var.realised_returns[asset_x],
                                                                    fund.var.ewma_returns[asset_x],
                                                                    fund.var.realised_returns[asset_y],
                                                                    fund.var.ewma_returns[asset_y],
                                                                    fund.var.covariance_matrix.loc[asset_x][asset_y],
                                                                    fund.par.price_memory)
    return new_covariance_matrix


def asset_expectations(fund, delta_news):
    """
    Update expected default rates and asset prices
    :param fund: object Fund for which to calculate expectations about asset prices and default rates
    :param delta_news: the change in the news process about asset default rates
    :return: dictionaries of expectated default rates and prices per asset
    """
    expected_default_rates = {}
    expected_prices = {}
    for asset in fund.var.assets:
        expected_default_rates[asset] = exp_default_rate(fund, asset, delta_news, fund.par.news_evaluation_error)
        expected_prices[asset] = exp_price_or_fx(asset.var.price, asset.var_previous.price,
                                                 fund.var.ewma_delta_prices[asset], fund.par.price_memory)
    return expected_default_rates, expected_prices


def currency_expectation(fund, fx_rates, previous_fx_rates):
    """
    Update several currency expectation
    :param fund: object Fund for which to calculate expectations about asset prices and default rates
    :param fx_rates: pandas DataFrame(index=currencies, columns=currencies) of current exchange rates
    :param previous_fx_rates: pandas Dataframe of previous period exchange rates
    :return: dictionaries of expected weighted moving average delta exchange rates,
    expected exchange rates and expected returns on currencies
    """
    ewma_delta_fx = {}
    exp_exchange_rates = {}
    exp_cash_returns = {}
    for currency in fund.var.currency:
        # add delta fx ewma
        current_fx = fx_rates.loc[fund.par.country][currency.par.country]
        previous_fx = previous_fx_rates.loc[fund.par.country][currency.par.country]
        realised_dfx =current_fx - previous_fx
        ewma_delta_fx[currency] = compute_ewma(realised_dfx, fund.var.ewma_delta_fx[currency],
                                                        fund.par.fx_memory)
        # calculate expected fx price
        exp_exchange_rates[currency] = exp_price_or_fx(current_fx, previous_fx,
                                                            fund.var.ewma_delta_fx[currency], fund.par.fx_memory)
        # calculate expected return on fx??
        exp_cash_returns[currency] = 2 # TODO add this

    return ewma_delta_fx, exp_exchange_rates, exp_cash_returns


def asset_return_expectations(fund, assets):
    """Update expectations for asset returns"""
    asset_ret_expectations = {}
    return asset_ret_expectations

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
