"""Main model"""
import numpy as np
import random

from functions.port_opt import *
from functions.asset_demands import *
from functions.ex_agent_asset_demands import *
from functions.balance_sheet_adjustments import *
from functions.stochasticprocess import *
from functions.expectation_formation import *
from functions.market_mechanism import *
from functions.profits_and_payouts import *
from functions.realised_returns import *


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
            fund.exp.default_rates = default_rate_expectations(fund, portfolios, delta_news)
            #fund.var.profits = hypothetical_asset_returns(fund, prices_tau, environment.var.fx_rates)[1]
            #fund.var.redeemable_shares = calculate_current_value_of_shares(fund, environment.var.fx_rates)
            #fund.var.redeemable_shares = payout_to_shareholders(fund)
            
            
        for tau in range(10): #TODO this needs to be rewritten into a while loop when stopping criteria are defined

            
            
            for fund in funds:
                

                # shareholder dividends and fund profits (returns)
                fund.var.profits, \
                fund.var.redeemable_shares, \
                fund.var.payouts = profit_and_payout(fund, portfolios, currencies, environment)
                
                # 1 Expectation formation
                fund.var.ewma_delta_prices, \
                fund.var.ewma_delta_fx, \
                fund.exp.prices, \
                fund.exp.exchange_rates = price_fx_expectations(fund, portfolios, currencies, environment)


                exp_returns, exp_cashreturns = return_expectations(fund, assets, environment)
                covariance, fund.var.ewma_returns = covariance_estimate(fund, assets, environment)
                
                
                fund.var.hypothetical_returns = hypothetical_asset_returns(fund, prices_tau, environment.var.fx_rates)[0]
                fund.var.ewma_returns, fund.var.ewma_delta_prices = asset_ewma(fund)
                fund.var.covariance_matrix = asset_covariances(fund)
                fund.exp.default_rates, fund.exp.prices = asset_expectations(fund, delta_news)

                fund.var.ewma_delta_fx, fund.exp.exchange_rates, \
                fund.exp.cash_returns = currency_expectation(fund, environment.var.fx_rates,
                                                             environment.var_previous.fx_rates)

                fund.exp.asset_returns = asset_return_expectations(fund, environment.var.fx_rates)


                # update the value of redeemable shares and payouts to share holders
                #fund.var.redeemable_shares = payouts_and_share_value(portfolios, currencies, fund, environment)
                                
                # compute the weights of optimal balance sheet positions

                fund.var.weights = portfolio_optimization(fund)
                
    
                # compute demand for balance sheet positions
                fund.var.asset_demand, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment, tau, day)


            # for ex in exogeneous_agents:
            #     exogeneous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogeneous_agents, portfolios )
            #
            #
            # for a in portfolios:
            #     a.var.price = price_adjustment(portfolios, currencies, environment, exogeneous_agents , funds, a)
            #
            # environment.var.fx_rates = fx_adjustment(portfolios, currencies, environment, exogeneous_agents , funds)
            
        #this is where intraday calculations end
        #for fund in funds:
            #fund.var.asset, fund.var.cash = balance_sheet_adjustment(funds, portfolios, currencies, exogeneous_agents)
        
      

