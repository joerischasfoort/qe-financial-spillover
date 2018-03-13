from objects.fund import *
from objects.asset import *
from objects.currency import *
from objects.environment import *
from objects.exogenous_agents import *
from functions.distribute import *
from functions.stochasticprocess import *
from functions.realised_returns import *
from functions.supercopy import copy_agent_variables
import numpy as np
import pandas as pd


def init_objects(parameters):
    """
    Function to initialise the model objects: first assets, then funds
    :param parameters: object which holds all model parameters
    :return: list of fund objects, list of asset objects
    """
    # 1 initialize assets
    portfolios = []
    total_assets = parameters["n_domestic_assets"] + parameters["n_foreign_assets"]
    asset_countries = ordered_list_of_countries(parameters["n_domestic_assets"], parameters["n_foreign_assets"])
    asset_return_variance = []
    asset_values = []
    default_rates = []
    returns = []

    for idx in range(total_assets):
        asset_params = AssetParameters(asset_countries[idx], parameters["face_value"],
                                       parameters["nominal_interest_rate"],
                                       parameters["maturity"], parameters["quantity"])
        init_asset_vars = AssetVariables(parameters["init_asset_price"], parameters["default_rate"])
        previous_assets_vars = AssetVariables(parameters["init_asset_price"], parameters["default_rate"])
        portfolios.append(Asset(idx, init_asset_vars, previous_assets_vars, asset_params))
        asset_return_variance.append(simulated_return_variance(portfolios[-1], parameters["days"], parameters))
        asset_values.append(portfolios[idx].var.price * portfolios[idx].par.quantity)
        default_rates.append(portfolios[idx].var.default_rate)
        returns.append(realised_profits_asset(portfolios[idx].var.default_rate, portfolios[idx].par.face_value,
                                              portfolios[idx].var.price, portfolios[idx].var.price,
                                              portfolios[idx].par.quantity, portfolios[idx].par.nominal_interest_rate,
                                              portfolios[idx].par.maturity))

    # 2 Initialize currencies
    currencies = []
    total_currency = parameters["total_money"]
    for idx, country in enumerate(set(asset_countries)):
        currency_param = CurrencyParameters(country, parameters["currency_rate"],
                                            np.divide(total_currency, len(set(asset_countries))))
        currencies.append(Currency(idx, currency_param))
        returns.append(parameters["currency_rate"])

    # 3 Create covariance matrix for assets
    covs = np.zeros((total_assets + len(currencies), total_assets + len(currencies)))
    # insert variance into the diagonal of the matrix
    for idx, var in enumerate(asset_return_variance):
        covs[idx][idx] = var

    assets = portfolios + currencies
    covariance_matrix = pd.DataFrame(covs, index=assets, columns=assets)

    # 4 Create funds
    funds = []
    total_funds = parameters["n_domestic_funds"] + parameters["n_foreign_funds"]
    fund_countries = ordered_list_of_countries(parameters["n_domestic_funds"], parameters["n_foreign_funds"])

    def divide_by_funds(variable): return np.divide(variable, total_funds)

    for idx in range(total_funds):
        cov_matr = covariance_matrix.copy()
        fund_params = AgentParameters(fund_countries[idx], parameters["price_memory"],
                                      parameters["fx_memory"], parameters["risk_aversion"],
                                      parameters["adaptive_param"], parameters["news_evaluation_error"],
                                      parameters["fund_target_growth"])
        asset_portfolio = {asset: divide_by_funds(value) for (asset, value) in zip(portfolios, asset_values)}
        asset_demand = {asset: parameters["init_asset_demand"] for asset, value in zip(portfolios, asset_values)}
        ewma_returns = {asset: rt for (asset, rt) in zip(assets, returns)}
        ewma_delta_prices = {asset: parameters["init_agent_ewma_delta_prices"] for (asset, rt) in zip(portfolios, returns)}
        ewma_delta_fx = {currency: parameters["init_ewma_delta_fx"] for currency in currencies}
        realised_rets = {asset: 0 for asset in assets}

        currency_portfolio = {}
        currency_demand = {}
        for currency in currencies:
            currency_demand[currency] = parameters["init_currency_demand"]
            if currency.par.country == fund_countries[idx]:
                # give this fund an initial amount of currency
                currency_portfolio[currency] = divide_by_funds(parameters["total_money"])
            else:
                currency_portfolio[currency] = 0
                # add the variance to covariance matrix
                cov_matr.loc[currency][currency] = parameters["fx_shock_std"]

        fund_vars = AgentVariables(asset_portfolio,
                                   currency_portfolio,
                                   sum(asset_portfolio.values()) + divide_by_funds(parameters["total_money"]),
                                   asset_demand,
                                   currency_demand,
                                   ewma_returns,
                                   ewma_delta_prices,
                                   ewma_delta_fx,
                                   cov_matr, parameters["init_payouts"], dict.fromkeys(assets),
                                   realised_rets, parameters["init_profits"])
        r = ewma_returns.copy()
        df_rates = {asset: default_rate for (asset, default_rate) in zip(portfolios, default_rates)}
        exp_prices = {asset: asset.var.price for asset in portfolios}
        exp_fx = {currency: parameters["init_exchange_rate"] for currency in currencies}
        exp_fx_returns = {currency: parameters["currency_rate"] for currency in currencies}
        fund_expectations = AgentExpectations(r, df_rates, exp_fx, exp_prices, exp_fx_returns)
        funds.append(Fund(idx, fund_vars,  copy_agent_variables(fund_vars), fund_params, fund_expectations))

    # 5 create environment with exchange rates
    fx_matrix = np.zeros([len(currencies), len(currencies)])
    fx_matrix = pd.DataFrame(fx_matrix, index=currencies, columns=currencies)

    for c1, c2 in zip(currencies, currencies[::-1]):
        fx = parameters["init_exchange_rate"]
        if c1.par.country == 'foreign':
            fx = 1 / fx
        fx_matrix.loc[c1, c2] = fx
        fx_matrix.loc[c1, c1] = 1

    currency_countries = {c: c.par.country for c in currencies}
    fx_matrix.rename(index=currency_countries, inplace=True)
    fx_matrix.rename(columns=currency_countries, inplace=True)

    environment = Environment(EnvironmentVariables(fx_matrix), EnvironmentVariables(fx_matrix.copy()),
                              EnvironmentParameters(parameters))

    # 6 create central bank
    cb_assets = {asset: 0 for asset in portfolios}
    cb_currency = {}
    for cur in currencies:
        if cur.par.country == parameters["cb_country"]:
            cb_currency[cur] = sum(cb_assets.values())
        else:
            cb_currency[cur] = 0

    asset_targets = {asset: 0 for asset in portfolios}
    cb_variables = CB_Variables(cb_assets, cb_currency, 0, 0, asset_targets)
    cb_previous = ExoAgentVariables(cb_assets.copy(), cb_currency.copy(), 0, 0)
    central_bank = Central_Bank(cb_variables, cb_previous, ExoAgentParameters(parameters["cb_country"]))

    # 7 create underwriter agent
    underwriter_assets = {asset: 0 for asset in portfolios}
    underwriter_currency = {currency: 0 for currency in currencies}
    underwriter_variables = ExoAgentVariables(underwriter_assets, underwriter_currency, 0, 0)
    underwriter_previous = ExoAgentVariables(underwriter_assets.copy(), underwriter_currency.copy(), 0, 0)
    underwriter = Underwriter(underwriter_variables, underwriter_previous)

    exogeneous_agents = {repr(central_bank): central_bank, repr(underwriter): underwriter}

    return portfolios, currencies, funds, environment, exogeneous_agents


def simulated_return_variance(asset, days, parameters):
    """
    Calculate an approximate variance for an asset by simulating the average underlying default probability
    :param asset: Asset object of interest
    :param days: integer amount of days over which to conduct the simulation
    :param parameters: dictionary with model parameters
    :return: float initial variance of the asset
    """
    simulated_default_rates = ornstein_uhlenbeck_levels(days, parameters["default_rate_mu"],
                                                        parameters["default_rate_delta_t"],
                                                        parameters["default_rate_std"],
                                                        parameters["default_rate_mean_reversion"])
    simulated_returns = [realised_profits_asset(df, face_value=asset.par.face_value, previous_price=1,
                                                price=1, quantity=asset.par.quantity,
                                                interest_rate=asset.par.nominal_interest_rate,
                                                maturity=asset.par.maturity) for df in simulated_default_rates]
    return np.var(simulated_returns)
