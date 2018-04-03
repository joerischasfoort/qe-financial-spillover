"""Main model"""
import numpy as np
import random
import copy
import pandas as pd
from functions.payouts_and_share_value import *
from functions.port_opt import *
from functions.asset_demands import *
from functions.ex_agent_asset_demands import *
from functions.balance_sheet_adjustments import *
from functions.stochasticprocess import *
from functions.expectation_formation import *
from functions.market_mechanism import *
from functions.profits_and_payouts import *
from functions.show import *
#from functions.realised_returns import *
from functions.supercopy import *


def spillover_model(portfolios, currencies, environment, exogeneous_agents, funds,  seed):
    """
    Koziol, Riedler & Schasfoort Agent-based simulation model of financial spillovers
    :param assets: list of Asset objects
    :param funds: list of Fund objects
    :param days: integer amount of days over which the simulation will take place
    :param seed: integer used to seed the random number generator
    :return: lists of assets, funds
    """
    random.seed(seed)
    np.random.seed(seed)
    # create tau data dictionary

    #Measurements
    data = {str(a) + 'price': [environment.par.global_parameters["init_asset_price"]] for a in portfolios}
    data["FX_rate_domestic_foreign"] = [environment.var.fx_rates.loc["domestic"][ "foreign"]]

    all_assets = portfolios + currencies
    for fund in funds:
        for a in portfolios:
            a_demands = {"a_demand_" + str(a) + "_fund_" + str(fund.name): [fund.var.asset_demand[a]] for demand in fund.var.asset_demand}
            data.update(a_demands)
        for c in currencies:
            c_demands = {"c_demand_" + str(c) + "_fund_" + str(fund.name): [fund.var.currency_demand[c]] for demand in fund.var.currency_demand}
            data.update(c_demands)
        for a in all_assets:
            exp_returns = {"exp_return_" + str(a) + "_fund_" + str(fund.name): [fund.exp.returns[a]] for return_ in fund.exp.returns}
            data.update(exp_returns)
            weights = { "weight_" +str(a) + "_fund_" + str(fund.name):  [fund.var.weights[a]]  for weight in fund.var.weights }
            data.update(weights)
            redeem_s = { "redeemable_shares" + "_fund_" + str(fund.name):  [fund.var.redeemable_shares]  }
            data.update(redeem_s)
    data["Delta_Capital"] = [0]

    news_process = ornstein_uhlenbeck_levels(environment.par.global_parameters["days"],
                                             environment.par.global_parameters["default_rate_mu"],
                                             environment.par.global_parameters["default_rate_std"],
                                             environment.par.global_parameters["default_rate_mean_reversion"])
    # We get the random noise 
    fx_shock = [ np.random.normal(0, environment.par.global_parameters["fx_shock_std"]) for i in range(environment.par.global_parameters["days"]) ]

    for a in portfolios:
        a.var.aux_ret = convert_P2R(a,a.var.price)
        if a.var.aux_ret<=0:
            a.var.aux_ret=0.0001

    for day in range(1, environment.par.global_parameters["days"]):
        # initialise intraday prices at current price
        delta_news = news_process[day] - news_process[day-1]

        # determine value and payouts to shareholders
        for fund in funds:
            fund.exp.default_rates = dr_expectations(fund, portfolios, delta_news)
            #print fund.exp.default_rates, day

        convergence=False
        intraday_over=False

        tau=0
        while intraday_over == False:
            tau += 1

            if convergence == True:
                intraday_over = True

            for fund in funds:
                # shareholder dividends and fund profits 
                fund.var.profits, \
                fund.var.redeemable_shares, \
                fund.var.payouts, testing = profit_and_payout(fund, portfolios, currencies, environment)

                # 1 Expectation formation
                fund.var.ewma_delta_prices, \
                fund.var.ewma_delta_fx, \
                fund.exp.prices, \
                fund.exp.exchange_rates = price_fx_expectations(fund, portfolios, currencies, environment)
                fund.exp.returns = return_expectations(fund, portfolios, currencies, environment)

                fund.var.ewma_returns, fund.var.covariance_matrix, fund.var.hypothetical_returns = covariance_estimate(fund, portfolios, environment, currencies)

                # compute the weights of optimal balance sheet positions
                fund.var.weights = portfolio_optimization(fund)

                # intermediate cash position resulting from interest payments, payouts, maturing and defaulting assets
                fund.var.currency_inventory = cash_inventory(fund, portfolios, currencies)

                # compute demand for balance sheet positions
                fund.var.asset_demand, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment)

            for ex in exogeneous_agents:
                exogeneous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogeneous_agents, portfolios )

            if intraday_over == False:
                Delta_Demand = {}
                for a in portfolios:
                    a.var.price, a.var.aux_ret, Delta_Demand[a] = price_adjustment(portfolios, environment, exogeneous_agents, funds, a)

                environment.var.fx_rates, Delta_Capital = fx_adjustment(portfolios, currencies, environment, exogeneous_agents , funds, 0.0)#fx_shock[day])
                #Delta_Capital = 0
            Deltas = {}
            Deltas.update(Delta_Demand)
            Deltas.update({"FX": Delta_Capital})
            convergence = sum(abs(Deltas[i])<0.0001 for i in Deltas)==len(Deltas) and tau >30


            print tau, convergence, Deltas

            #Update intraday data points
            for a in portfolios:
                data[str(a) + 'price'].append(a.var.price) #TODO remove when done


            for fund in funds:
                data["redeemable_shares" + "_fund_" + str(fund.name)].append(fund.var.redeemable_shares)
                for a in portfolios:
                    data["a_demand_" + str(a) + "_fund_" + str(fund.name)].append(fund.var.asset_demand[a])
                for c in currencies:
                    data["c_demand_" + str(c) + "_fund_" + str(fund.name)].append(fund.var.currency_demand[c])

                for a in all_assets:
                    data["weight_" + str(a) + "_fund_" + str(fund.name)].append(fund.var.weights[a])
                    data["exp_return_" + str(a) + "_fund_" + str(fund.name)].append(fund.exp.returns[a])

            data["Delta_Capital"].append(Delta_Capital )
            data["FX_rate_domestic_foreign"].append(environment.var.fx_rates.loc["domestic"][ "foreign"])
            #this is where intraday calculations end


        #computing new asset and cash positions
        excess_demand, pi, nu = asset_excess_demand_and_correction_factors(funds, portfolios, currencies, exogeneous_agents)

         # trading
        for fund in funds:
            fund.var.assets = fund_asset_adjustments(fund, portfolios, excess_demand, pi, nu)
            fund.var.currency_inventory = fund_cash_inventory_adjustment(fund, portfolios, currencies)

        for ex in exogeneous_agents:
            exogeneous_agents[ex].var.assets = ex_asset_adjustments(ex, portfolios, excess_demand, pi, nu, exogeneous_agents)

        # balance sheet adjustment
        for fund in funds:
            fund.var.currency_demand = cash_demand_correction(fund, currencies,environment)

        nuC, piC, excess_demandC = cash_excess_demand_and_correction_factors(funds, currencies)


        for fund in funds:
            fund.var.currency = fund_cash_adjustments(nuC, piC, excess_demandC, currencies, fund)

        #debugging
        show_fund(funds[0], portfolios, currencies, environment)
        show_fund(funds[1], portfolios, currencies, environment)


        # update previous variables
        for fund in funds:
            fund.var_previous = copy_agent_variables(fund.var)

        for portfolio in portfolios:
            portfolio.var_previous = copy.copy(portfolio.var)

        environment.var_previous = copy_env_variables(environment.var)

        exogeneous_agents['central_bank_domestic'].var_previous = copy_cb_variables(exogeneous_agents['central_bank_domestic'].var)
        exogeneous_agents['underwriter'].var_previous = copy_underwriter_variables(exogeneous_agents['underwriter'].var)


    pd.DataFrame(data).to_csv('intraday_data.csv')

    return portfolios, currencies, environment, exogeneous_agents, funds