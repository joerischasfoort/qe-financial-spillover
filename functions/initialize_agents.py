from objects.fund import *
from functions.distribute import *
import pandas as pd
from functions.supercopy import copy_agent_variables
from functions.stochasticprocess import *
from objects.exogenous_agents import *
from functions.realised_returns import *


def init_funds(environment, portfolios, currencies, parameters):

    funds = []
    total_funds = parameters["n_domestic_funds"] + parameters["n_foreign_funds"]
    fund_countries = ordered_list_of_countries(parameters["n_domestic_funds"], parameters["n_foreign_funds"])


    for idx in range(total_funds):

        fund_params = AgentParameters(fund_countries[idx], parameters["price_memory"],
                                      parameters["fx_memory"], parameters["risk_aversion"],
                                      parameters["adaptive_param"], parameters["news_evaluation_error"])

        # compute initial variable values associated with portfolio shares
        asset_portfolio = {}
        asset_demand = {}
        ewma_returns = {}
        ewma_delta_prices = {}
        realised_rets = {}

        for a in portfolios:

            # funds initially have a home bias of 100%
            if fund_countries[idx]==a.par.country:
                asset_portfolio.update({a: a.par.quantity / sum([i==a.par.country for i in fund_countries])})
            else:
                asset_portfolio.update({a: 0})


            asset_demand.update({a: 0})  # demand is initialized at zero (this does not effect anything)
            ewma_returns.update({a: a.par.nominal_interest_rate}) # the nominal interest rate is the initial return
            ewma_delta_prices.update({a: parameters["init_agent_ewma_delta_prices"]}) #TODO: IS THIS STILL NEEDED? WHY IS THE INITIAL VALUE 1?
            realised_rets.update({a: 0})





        # compute initial variable values associated with currencies
        currency_portfolio = {}
        currency_inventory = {}
        currency_demand = {}
        ewma_delta_fx = {}
        losses = {}

        for currency in currencies:
            # funds initially have a home bias of 100%
            if fund_countries[idx]==currency.par.country:
                currency_portfolio.update({currency: currency.par.quantity / sum([i==currency.par.country for i in fund_countries])})
            else:
                currency_portfolio.update({currency: 0})

            currency_inventory.update({currency: 0}) #TODO: could this also be empty

            currency_demand.update({currency: parameters["init_currency_demand"]}) #Todo: could this be empty

            ewma_delta_fx.update({currency: parameters["init_ewma_delta_fx"]}) #TODO: Still needed?

            ewma_returns.update({currency: currency.par.nominal_interest_rate}) # the nominal interest rate is the initial return


            losses.update({currency: parameters["init_losses"]})



        # initialized as having no value
        init_c_profits = dict.fromkeys(currencies)
        init_a_profits = dict.fromkeys(portfolios)
        init_profits = init_c_profits.copy()  # start with x's keys and values
        init_profits.update(init_a_profits)

        assets = portfolios + currencies
        covs = np.zeros((len(assets), len(assets)))
        cov_matr = pd.DataFrame(covs, index=assets, columns=assets)


        fund_redeemable_share_size = [asset_portfolio[a] * a.var.price * environment.var.fx_rates.loc[fund_countries[idx]][a.par.country] for a in portfolios] + [currency_portfolio[c] * environment.var.fx_rates.loc[fund_countries[idx]][c.par.country] for c in currencies]
        fund_redeemable_share_size = sum(fund_redeemable_share_size)

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



        #Initialising expectations
        r = ewma_returns.copy()
        df_rates = {a: a.var.default_rate for a in portfolios}
        exp_prices = {a: a.var.price for a in portfolios}
        exp_fx = environment.var.fx_rates.copy()
        exp_fx_returns = {currency: currency.par.nominal_interest_rate for currency in currencies}

        fund_expectations = AgentExpectations(r, df_rates, exp_fx, exp_prices, exp_fx_returns) #TODO: why is this called exp_fx_returns? In the object this variable is called cash return


        funds.append(Fund(idx, fund_vars, copy_agent_variables(fund_vars), fund_params, fund_expectations))

    #initialize the covariance matrix with simulated values
    simulated_time_series = simulated_asset_return(funds, portfolios, currencies, 10000,
                                                   parameters)
    for fund in funds:
        for i in assets:
            for j in assets:
                fund.var.covariance_matrix.loc[i, j] = \
                np.cov(simulated_time_series[fund][i], simulated_time_series[fund][j])[0][1]



    return funds
















def init_exogenous_agents(portfolios, currencies, parameters):
    # create central bank
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

    # create underwriter agent
    underwriter_assets = {asset: 0 for asset in portfolios}
    underwriter_currency = {currency: 0 for currency in currencies}
    underwriter_variables = ExoAgentVariables(underwriter_assets, underwriter_currency, 0, 0)
    underwriter_previous = ExoAgentVariables(underwriter_assets.copy(), underwriter_currency.copy(), 0, 0)
    underwriter = Underwriter(underwriter_variables, underwriter_previous)

    exogeneous_agents = {repr(central_bank): central_bank, repr(underwriter): underwriter}

    return exogeneous_agents











def simulated_asset_return(funds,portfolios, currencies, days, parameters):
    TS_for_funds = {}
    for asset in portfolios:
        #compute default rates for an asset
        TS_default_rates, fundamental_default_rate_expectation = exogenous_defaults(parameters, asset, days,seed=1)

        #compute inflation and fx shocks
        exogenous_shocks = correlated_shocks(parameters, days,seed=1)

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
