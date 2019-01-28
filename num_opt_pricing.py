
from functions.port_opt import *
from functions.asset_demands import *
from functions.ex_agent_asset_demands import *
from functions.stochasticprocess import *
from functions.expectation_formation import *
from functions.market_mechanism import *
from functions.profits_and_payouts import *
import numpy as np


def NOP(X, funds,portfolios,currencies, environment, exogeneous_agents, day, fx_shock):
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

    for ex in exogeneous_agents:
        exogeneous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogeneous_agents, portfolios)


    # Update prices if convergence has not been achieved yet
    var = []
    portfolios, environment, Deltas = update_market_prices_and_fx(portfolios, currencies, environment,
                                                                      exogeneous_agents, funds, var)

    # calculating and printing degree(in percent) to which the convergence bound is reached. Values <= zero need to be achieved
    list_DeltasA = [abs(Deltas[a]) for a in portfolios]
    mean_DA = np.mean(np.array(list_DeltasA))
    max_DA = np.max(np.array(list_DeltasA))
    FX_DA = abs(np.array(Deltas['FX']))
    print ("day:", day, "tau:", tau, "mean_A:", mean_DA, 'max_A:', max_DA, 'FX:', FX_DA)

    return mean_DA+FX_DA