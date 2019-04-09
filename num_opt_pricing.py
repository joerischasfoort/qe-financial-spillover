
from functions.port_opt import *
from functions.asset_demands import *
from functions.ex_agent_asset_demands import *
from functions.stochasticprocess import *
from functions.expectation_formation import *
from functions.market_mechanism import *
from functions.profits_and_payouts import *
import numpy as np


def NOP(X, funds, portfolios, currencies, environment, exogenous_agents, day, fx_shock):
    for a in portfolios:
        id_a=int(filter(str.isdigit, str(a)))
        a.var.price = X[id_a]
    environment.var.fx_rates.iloc[0][1] = X[-1]
    environment.var.fx_rates.iloc[1][0] = 1 / X[-1]


    for fund in funds:
        # shareholder dividends and fund profits
        fund.var.profits, \
        fund.var.cons_profits, \
        fund.var.losses, \
        fund.var.redeemable_shares, \
        fund.var.payouts = profit_and_payout(fund, portfolios, currencies, environment)

        # Expectation formation
        fund.var.ewma_delta_prices, \
        fund.var.ewma_delta_fx, \
        fund.exp.prices, \
        fund.exp.exchange_rates = price_fx_expectations(fund, portfolios, currencies, environment)

        fund.exp.exchange_rates, fund.exp.exchange_rate_anchor = anchored_FX_expectations(fund, environment, fx_shock)

        fund.exp.returns = return_expectations(fund, portfolios,
                                                                                                       currencies,
                                                                                                     environment)

        tau=1

        # compute the weights of optimal balance sheet positions
        fund.var.weights = portfolio_optimization_KT(fund, day, tau)

        # intermediate cash position resulting from interest payments, payouts, maturing and defaulting assets
        fund.var.currency_inventory = cash_inventory(fund, portfolios, currencies)

        # compute demand for balance sheet positions
        fund.var.asset_demand, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment)

    for ex in exogenous_agents:
        exogenous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogenous_agents, portfolios)


    # Update prices if convergence has not been achieved yet
    var = []
    portfolios, environment, Deltas = update_market_prices_and_fx(portfolios, currencies, environment,
                                                                  exogenous_agents, funds, var)

    # calculating and printing degree(in percent) to which the convergence bound is reached. Values <= zero need to be achieved
    list_DeltasA = [abs(Deltas[a]) for a in portfolios]
    mean_DA = np.mean(np.array(list_DeltasA))
    max_DA = np.max(np.array(list_DeltasA))
    FX_DA = abs(np.array(Deltas['FX']))
    print ("day:", day, "tau:", tau, "mean_A:", mean_DA, 'max_A:', max_DA, 'FX:', FX_DA)

    return mean_DA+FX_DA


def optimal_asset_prices_one_country(X, funds, portfolios, currencies, parameters, exogenous_agents, day):
    """
    Function to find equilibrium asset prices through numerical optimization.
    :param X: np.array of prices
    :param funds: list of Fund objects
    :param portfolios: list of portfolio objects
    :param currencies: list of currency objects
    :param parameters: dictionary with model parameters
    :param exogenous_agents: list containing the underwriter agent and central bank
    :param day: integer of the simulated day
    :return: float average excess demand
    """
    total_asset_demand = [0 for a in portfolios]

    # set the price of the portfolio's equal to the input prices
    for idx, a in enumerate(portfolios):
        #id_a = int(filter(str.isdigit, str(a)))
        a.var.price = X[idx]

    for fund in funds:
        # shareholder dividends and fund profits TODO change to
        fund.var.profits, \
        fund.var.losses, \
        fund.var.redeemable_shares, \
        fund.var.payouts = profit_and_payout_oc(fund, portfolios, currencies, parameters) #TODO debug

        # Expectation formation
        fund.var.ewma_delta_prices, fund.exp.prices = price_expectations(fund, portfolios) #TODO debug

        fund.exp.returns = return_expectations_oc(fund, portfolios, currencies, parameters) #TODO update

        tau = 1

        # compute the weights of optimal balance sheet positions
        fund.var.weights = portfolio_optimization_KT(fund, day, tau)

        # intermediate cash position resulting from interest payments, payouts, maturing and defaulting assets
        fund.var.currency_inventory = cash_inventory(fund, portfolios, currencies)  # TODO debug

        # compute demand for balance sheet positions
        fund.var.asset_demand, fund.var.currency_demand = asset_demand_oc(fund, portfolios, currencies)  #TODO debug

    for ex in exogenous_agents:
        exogenous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogenous_agents, portfolios)

    for idx, a in enumerate(portfolios):
        # add excess demand
        demand = 0
        for fund in funds:
            demand += fund.var.asset_demand[a]
        for ex in exogenous_agents:
            demand += ex.var.asset_demand[a]

        total_asset_demand[idx] = demand

    # Update prices if convergence has not been achieved yet
    #var = []
    #portfolios, environment, Deltas = update_market_prices(portfolios, exogeneous_agents, funds) #TODO do I need var?, update market prices and fx

    # calculating and printing degree(in percent) to which the convergence bound is reached. Values <= zero need to be achieved
    # list_DeltasA = [abs(Deltas[a]) for a in portfolios]
    # mean_DA = np.mean(np.array(list_DeltasA))
    # max_DA = np.max(np.array(list_DeltasA))
    # print("day:", day, "tau:", tau, "mean_A:", mean_DA, 'max_A:', max_DA)

    return np.mean(total_asset_demand)
