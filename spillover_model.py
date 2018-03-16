"""Main model"""
import numpy as np
import random
import copy

from functions.port_opt import *
from functions.asset_demands import *
from functions.ex_agent_asset_demands import *
from functions.balance_sheet_adjustments import *
from functions.stochasticprocess import *
from functions.expectation_formation import *
from functions.market_mechanism import *
from functions.profits_and_payouts import *
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

    news_process = ornstein_uhlenbeck_levels(environment.par.global_parameters["days"],
                                             environment.par.global_parameters["default_rate_mu"],
                                             environment.par.global_parameters["default_rate_delta_t"],
                                             environment.par.global_parameters["default_rate_std"],
                                             environment.par.global_parameters["default_rate_mean_reversion"])

    for day in range(1, environment.par.global_parameters["days"]):
        # initialise intraday prices at current price
        prices_tau = {portfolio: portfolio.var.price for portfolio in portfolios}
        delta_news = news_process[day] - news_process[day-1]

        # determine value and payouts to shareholders
        for fund in funds:
            fund.exp.default_rates = dr_expectations(fund, portfolios, delta_news)
            
        for tau in range(100): #TODO this needs to be rewritten into a while loop when stopping criteria are defined

            for fund in funds:
                # shareholder dividends and fund profits 
                fund.var.profits, \
                fund.var.redeemable_shares, \
                fund.var.payouts = profit_and_payout(fund, portfolios, currencies, environment)
                
                # 1 Expectation formation
                fund.var.ewma_delta_prices, \
                fund.var.ewma_delta_fx, \
                fund.exp.prices, \
                fund.exp.exchange_rates = price_fx_expectations(fund, portfolios, currencies, environment)
                fund.exp.asset_returns, fund.exp.cash_returns = return_expectations(fund, portfolios, currencies, environment)
                fund.var.ewma_returns, fund.var.covariance_matrix = covariance_estimate(fund, portfolios)

                              
                # compute the weights of optimal balance sheet positions
                fund.var.weights = portfolio_optimization(fund)
                
                # intermediate cash position resulting from interest payments, payouts, maturing and defaulting assets
                fund.var.currency_inventory = cash_inventory(fund, portfolios, currencies)
                
                # compute demand for balance sheet positions
                fund.var.asset_demand, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment)


            for ex in exogeneous_agents:
                exogeneous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogeneous_agents, portfolios )
            
            for a in portfolios:
                a.var.price = price_adjustment(portfolios, environment, exogeneous_agents , funds, a)
             
            environment.var.fx_rates = fx_adjustment(portfolios, currencies, environment, exogeneous_agents , funds) #exchange rate adjustment
    
    
            print a.var.price, fund.exp.prices
    #this is where intraday calculations end
        
        #computing new asset and cash positions
        excess_demand, pi, nu = asset_excess_demand_and_correction_factors(funds, portfolios, currencies, exogeneous_agents)
    
        for fund in funds:
            fund.var.assets = fund_asset_adjustments(fund, portfolios, excess_demand, pi, nu)
        
        for ex in exogeneous_agents:
            exogeneous_agents[ex].var.assets = ex_asset_adjustments(ex, portfolios, excess_demand, pi, nu, exogeneous_agents)
        
        nuC, piC, excess_demandC = cash_excess_demand_and_correction_factors(funds, portfolios, currencies, exogeneous_agents)
        
        for fund in funds:
            fund.var.currency = fund_cash_adjustments(nuC, piC, excess_demandC, currencies, fund, portfolios)

        # update previous variables
        for fund in funds:
            fund.var_previous = copy_agent_variables(fund.var)

        for portfolio in portfolios:
            portfolio.var_previous = copy.copy(portfolio.var)

        exogeneous_agents['central_bank_domestic'].var_previous = copy_cb_variables(exogeneous_agents['central_bank_domestic'].var)
        exogeneous_agents['underwriter'].var_previous = copy_underwriter_variables(exogeneous_agents['underwriter'].var)

    return portfolios, currencies, environment, exogeneous_agents, funds
