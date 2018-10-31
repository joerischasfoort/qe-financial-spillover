from objects.fund import *
from functions.distribute import *
import pandas as pd
from functions.supercopy import copy_agent_variables
from functions.stochasticprocess import *
from objects.exogenous_agents import *
from functions.realised_returns import *


def init_funds(environment, portfolios, currencies, parameters, seed):

    funds = []
    total_funds = parameters["n_domestic_funds"] + parameters["n_foreign_funds"]
    fund_countries = ordered_list_of_countries(parameters["n_domestic_funds"], parameters["n_foreign_funds"])


    for idx in range(total_funds):
        risk_aversion = {"domestic_assets": parameters[fund_countries[idx]+"_risk_aversion_D_asset"],
                         "foreign_assets": parameters[fund_countries[idx] + "_risk_aversion_F_asset"]}
        fund_params = AgentParameters(fund_countries[idx], parameters["price_memory"],
                                      parameters["fx_memory"], risk_aversion,
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
        cons_returns = {a: 0 for a in portfolios + currencies}
        df_rates = {a: a.var.default_rate for a in portfolios}
        exp_prices = {a: a.var.price for a in portfolios}
        exp_fx = environment.var.fx_rates.copy()
        exp_fx_anchor = environment.var.fx_rates.copy()
        exp_fx_returns = {currency: currency.par.nominal_interest_rate for currency in currencies}
        exp_inflation = {"domestic":parameters["domestic_inflation_mean"],"foreign":parameters["foreign_inflation_mean"]}
        fund_expectations = AgentExpectations(r,cons_returns, r, df_rates, exp_fx, exp_fx_anchor, exp_prices, exp_fx_returns, exp_inflation) #TODO: why is this called exp_fx_returns? In the object this variable is called cash return

        funds.append(Fund(idx, fund_vars, copy_agent_variables(fund_vars), fund_params, fund_expectations))

    #initialize the covariance matrix with simulated values
    simulated_time_series = simulated_asset_return(funds, portfolios, currencies, 10000,
                                                   parameters, seed)
    for fund in funds:
        for i in assets:
            for j in assets:
                fund.var.covariance_matrix.loc[i][j] = np.cov(simulated_time_series[fund][i], simulated_time_series[fund][j])[0][1]

        fund.var_previous.covariance_matrix = fund.var.covariance_matrix.copy()

    return funds





def init_funds_4a(environment, portfolios, p_holdings_4a, currencies, c_holdings_4a, parameters, risk_aversions_4a, seed):

    funds = []
    total_funds = parameters["n_domestic_funds"] + parameters["n_foreign_funds"]
    fund_countries = ordered_list_of_countries(parameters["n_domestic_funds"], parameters["n_foreign_funds"])

    dom_funds=0
    for_funds=0
    for idx in range(total_funds):
        # compute initial variable values associated with portfolio shares
        asset_portfolio = {}
        asset_demand = {}
        ewma_returns = {}
        ewma_delta_prices = {}
        realised_rets = {}

        for ii, a in enumerate(portfolios):
            # funds initially have a home bias of 100%
            if fund_countries[idx]=="domestic":
                asset_portfolio.update({a: p_holdings_4a["domestic_"+str(dom_funds)][ii]})

            else:
                asset_portfolio.update({a: p_holdings_4a["foreign_" + str(for_funds)][ii]})



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

        for ii, currency in enumerate(currencies):
            # funds initially have a home bias of 100%
            if fund_countries[idx]=="domestic":
                currency_portfolio.update({currency: c_holdings_4a["domestic_"+str(dom_funds)][ii]})
            else:
                currency_portfolio.update({currency: c_holdings_4a["foreign_" + str(for_funds)][ii]})

            currency_inventory.update({currency: 0}) #TODO: could this also be empty

            currency_demand.update({currency: parameters["init_currency_demand"]}) #Todo: could this be empty

            ewma_delta_fx.update({currency: parameters["init_ewma_delta_fx"]}) #TODO: Still needed?

            ewma_returns.update({currency: currency.par.nominal_interest_rate}) # the nominal interest rate is the initial return

            losses.update({currency: parameters["init_losses"]})

        if fund_countries[idx] == "domestic":
            risk_aversion = {ra.split("aversion_")[-1]: risk_aversions_4a[ra][dom_funds] for ra in ['domestic_risk_aversion_domestic_asset', 'domestic_risk_aversion_foreign_asset']}
            dom_funds += 1
        if fund_countries[idx] == "foreign":
            risk_aversion = {ra.split("aversion_")[-1]: risk_aversions_4a[ra][for_funds] for ra in ['foreign_risk_aversion_domestic_asset', 'foreign_risk_aversion_foreign_asset']}
            for_funds += 1

        fund_params = AgentParameters(fund_countries[idx], parameters["price_memory"],
                                      parameters["fx_memory"], risk_aversion,
                                      parameters["adaptive_param"], parameters["news_evaluation_error"])


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
        cons_returns = {a: 0 for a in portfolios + currencies}
        df_rates = {a: a.var.default_rate for a in portfolios}
        exp_prices = {a: a.var.price for a in portfolios}
        exp_fx = environment.var.fx_rates.copy()
        exp_fx_anchor = environment.var.fx_rates.copy()
        exp_fx_returns = {currency: currency.par.nominal_interest_rate for currency in currencies}
        exp_inflation = {"domestic":parameters["domestic_inflation_mean"],"foreign":parameters["foreign_inflation_mean"]}
        fund_expectations = AgentExpectations(r,cons_returns, r, df_rates, exp_fx, exp_fx_anchor, exp_prices, exp_fx_returns, exp_inflation) #TODO: why is this called exp_fx_returns? In the object this variable is called cash return

        funds.append(Fund(idx, fund_vars, copy_agent_variables(fund_vars), fund_params, fund_expectations))

    #initialize the covariance matrix with simulated values
    simulated_time_series = simulated_asset_return(funds, portfolios, currencies, 10000,
                                                   parameters, seed)
    for fund in funds:
        for i in assets:
            for j in assets:
                fund.var.covariance_matrix.loc[i][j] = np.cov(simulated_time_series[fund][i], simulated_time_series[fund][j])[0][1]

        fund.var_previous.covariance_matrix = fund.var.covariance_matrix.copy()

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

    fx_interventionist_asset_demand = {asset: 0 for asset in portfolios}
    fx_interventionist_currency  = {currency: 0 for currency in currencies}
    fx_interventionist_currency_demand  = {currency: 0 for currency in currencies}
    fx_interventionist_variables = FX_Interventionist_Variables(fx_interventionist_asset_demand, fx_interventionist_currency,fx_interventionist_currency_demand)
    fx_interventionist = FX_Interventionist(fx_interventionist_variables)






    exogeneous_agents = {repr(central_bank): central_bank, repr(underwriter): underwriter, repr(fx_interventionist): fx_interventionist}





    return exogeneous_agents











def simulated_asset_return(funds,portfolios, currencies, days, parameters,seed):
    TS_for_funds = {}
    TS_default_rates = {}
    fundamental_default_rate_expectation = {}
    for asset in portfolios:
        #compute default rates for an asset
        TS_default_rates[asset], fundamental_default_rate_expectation[asset] = exogenous_defaults(parameters, asset, days, seed)

        #compute inflation and fx shocks
        exogenous_shocks = correlated_shocks(parameters, days,seed)

    for fund in funds:
        simulated_real_returns = {}
        simulated_nominal_returns = {}
        for asset in portfolios:
            if fund.par.country == asset.par.country:
                new_fx = [1 for idx in range(days)]
            if fund.par.country != asset.par.country:
                if asset.par.country == "foreign":
                    new_fx = 1+np.array(exogenous_shocks["fx_shock"])
                if asset.par.country == "domestic":
                    new_fx = 1/(1+np.array(exogenous_shocks["fx_shock"]))
            simulated_nominal_returns[asset] = np.array([realised_profits_asset(df, face_value=asset.par.face_value, previous_price=1,
                                                    price=1, quantity=asset.par.quantity,
                                                    interest_rate=asset.par.nominal_interest_rate,
                                                    maturity=asset.par.maturity, previous_exchange_rate=1, exchange_rate=new_fx[idx]) for idx, df in enumerate(TS_default_rates[asset])])
            if asset.par.maturity < 1:
                simulated_real_returns[asset] = ((1+simulated_nominal_returns[asset]) / (1+exogenous_shocks[asset.par.country + "_inflation"]))-1
            else:
                simulated_real_returns[asset] = simulated_nominal_returns[asset]


        for cur in currencies:
            if fund.par.country == cur.par.country:
                new_fx = [1 for idx in range(days)]
            if fund.par.country != cur.par.country:
                if cur.par.country == "foreign":
                    new_fx = 1+np.array(exogenous_shocks["fx_shock"])
                if cur.par.country == "domestic":
                    new_fx = 1/(1+np.array(exogenous_shocks["fx_shock"]))

            simulated_nominal_returns[cur] = np.array([realised_profits_currency(cur.par.nominal_interest_rate, previous_exchange_rate=1, exchange_rate=new_fx[idx]) for idx, df in enumerate(new_fx)])
            simulated_real_returns[cur] = ((1+simulated_nominal_returns[cur]) / (1+exogenous_shocks[cur.par.country + "_inflation"]))-1



        TS_for_funds[fund]=simulated_real_returns

    return TS_for_funds
