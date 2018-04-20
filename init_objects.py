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
        init_asset_vars = AssetVariables(parameters["init_asset_price"],
                                         0 # initial default rate
                                         )
        previous_assets_vars = AssetVariables(parameters["init_asset_price"],
                                              0  # initial default rate
                                              )
        portfolios.append(Asset(idx, init_asset_vars, previous_assets_vars, asset_params))
        #####
        #asset_return_variance.append(simulated_return_variance(portfolios[-1], 10000, parameters))
        asset_values.append(portfolios[idx].var.price * portfolios[idx].par.quantity)
        default_rates.append(portfolios[idx].var.default_rate)
        returns.append(realised_profits_asset(portfolios[idx].var.default_rate, portfolios[idx].par.face_value,
                                              portfolios[idx].var.price, portfolios[idx].var.price,
                                              portfolios[idx].par.quantity, portfolios[idx].par.nominal_interest_rate,
                                              portfolios[idx].par.maturity,previous_exchange_rate=1,exchange_rate=1))

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

    ######
    #for idx, var in enumerate(asset_return_variance):
    #    covs[idx][idx] = var

    assets = portfolios + currencies
    covariance_matrix = pd.DataFrame(covs, index=assets, columns=assets)

    # 4 create environment with exchange rates
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

    # 5 Create funds
    funds = []
    total_funds = parameters["n_domestic_funds"] + parameters["n_foreign_funds"]
    fund_countries = ordered_list_of_countries(parameters["n_domestic_funds"], parameters["n_foreign_funds"])

    def divide_by_funds(variable): return np.divide(variable, total_funds)

    for idx in range(total_funds):
        cov_matr = covariance_matrix.copy()
        # change covariance to include exchange rate movements
        for a in portfolios:
            if a.par.country != fund_countries[idx]:
                cov_matr.loc[a, a] = cov_matr.loc[a, a] + parameters["fx_shock_std"]**2

        fund_params = AgentParameters(fund_countries[idx], parameters["price_memory"],
                                      parameters["fx_memory"], parameters["risk_aversion"],
                                      parameters["adaptive_param"], parameters["news_evaluation_error"])
        asset_portfolio = {asset: divide_by_funds(value) for (asset, value) in zip(portfolios, asset_values)}
        asset_demand = {asset: parameters["init_asset_demand"] for asset, value in zip(portfolios, asset_values)}
        ewma_returns = {asset: rt for (asset, rt) in zip(assets, returns)}
        ewma_delta_prices = {asset: parameters["init_agent_ewma_delta_prices"] for (asset, rt) in zip(portfolios, returns)}
        ewma_delta_fx = {currency: parameters["init_ewma_delta_fx"] for currency in currencies}
        realised_rets = {asset: 0 for asset in assets}
        init_c_profits = dict.fromkeys(currencies)
        init_a_profits = dict.fromkeys(assets)
        init_profits = init_c_profits.copy()  # start with x's keys and values
        init_profits.update(init_a_profits)
        currency_inventory = {currency: 0 for currency in currencies}
        currency_portfolio = {}
        currency_demand = {}
        losses = {}

        for currency in currencies:
            currency_demand[currency] = parameters["init_currency_demand"]
            losses[currency] = parameters["init_losses"]
            if currency.par.country == fund_countries[idx]:
                # give this fund an initial amount of currency
                amount = divide_by_funds(parameters["total_money"])
                currency_portfolio[currency] = 0.5 * amount
            else:
                amount = divide_by_funds(parameters["total_money"])
                currency_portfolio[currency] = 0.5 * amount

                # add the variance to covariance matrix
                cov_matr.loc[currency][currency] = parameters["fx_shock_std"]**2

        for i in currencies + portfolios:
            for j in currencies + portfolios:
                if i.par.country == j.par.country:
                    cov_matr.loc[i,j]=cov_matr.loc[i,j]+parameters[i.par.country + "_inflation_std"]**2


        fund_redeemable_share_size = sum(asset_portfolio.values()) + divide_by_funds(parameters["total_money"])
         
        fund_vars = AgentVariables(asset_portfolio,
                                   currency_portfolio,
                                   fund_redeemable_share_size,
                                   asset_demand,
                                   currency_demand,
                                   ewma_returns,
                                   ewma_delta_prices,
                                   ewma_delta_fx,
                                   cov_matr, parameters["init_payouts"], dict.fromkeys(assets),
                                   realised_rets, init_profits, losses,
                                   fund_redeemable_share_size,
                                   currency_inventory)
 
        r = ewma_returns.copy()
        df_rates = {asset: default_rate for (asset, default_rate) in zip(portfolios, default_rates)}
        exp_prices = {asset: asset.var.price for asset in portfolios}
        exp_fx = fx_matrix.copy()
        exp_fx_returns = {currency: parameters["currency_rate"] for currency in currencies}
        fund_expectations = AgentExpectations(r, df_rates, exp_fx, exp_prices, exp_fx_returns)
        funds.append(Fund(idx, fund_vars,  copy_agent_variables(fund_vars), fund_params, fund_expectations))


    # create covariance matrix
    simulated_time_series = simulated_asset_return(funds, portfolios, currencies, 10000, parameters)
    for fund in funds:
        for i in assets:
            for j in assets:
                fund.var.covariance_matrix.loc[i,j]=np.cov(simulated_time_series[fund][i],simulated_time_series[fund][j])[0][1]





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


def simulated_asset_return(funds,portfolios, currencies, days, parameters):
    TS_for_funds = {}
    for asset in portfolios:
        #compute default rates for an asset
        TS_default_rates, fundamental_default_rate_expectation = exogenous_defaults(parameters, asset, days)

        #compute inflation and fx shocks
        exogenous_shocks = correlated_shocks(parameters, days)

    for fund in funds:
        simulated_real_returns = {}
        for asset in portfolios:
            if fund.par.country == asset.par.country:
                new_fx = [1 for idx, val in enumerate(TS_default_rates)]
            if fund.par.country != asset.par.country:
                if asset.par.country == "foreign":
                    new_fx = [(1+exogenous_shocks["fx_shock"][idx]) for idx, val in enumerate(TS_default_rates)]
                if asset.par.country == "domestic":
                    new_fx = [1/(1+exogenous_shocks["fx_shock"][idx]) for idx, val in enumerate(TS_default_rates)]

            simulated_nominal_returns = [realised_profits_asset(df, face_value=asset.par.face_value, previous_price=1,
                                                    price=1, quantity=asset.par.quantity,
                                                    interest_rate=asset.par.nominal_interest_rate,
                                                    maturity=asset.par.maturity, previous_exchange_rate=1, exchange_rate=new_fx[idx]) for idx, df in enumerate(TS_default_rates)]

            simulated_real_returns[asset] = [((1+simulated_nominal_returns[idx])/(1+exogenous_shocks[asset.par.country + "_inflation"][idx]))-1 for idx, val in enumerate(simulated_nominal_returns)]

        for cur in currencies:
            simulated_nominal_returns = [realised_profits_currency(cur.par.nominal_interest_rate, previous_exchange_rate=1, exchange_rate=new_fx[idx]) for idx, df in enumerate(TS_default_rates)]
            simulated_real_returns[cur] = [
                ((1 + simulated_nominal_returns[idx]) / (1 + exogenous_shocks[cur.par.country + "_inflation"][idx])) - 1
                for idx, val in enumerate(simulated_nominal_returns)]

        TS_for_funds[fund]=simulated_real_returns

    return TS_for_funds
