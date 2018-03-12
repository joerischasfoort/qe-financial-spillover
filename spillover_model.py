"""Main model"""
import numpy as np
import random

from functions.port_opt import *
from functions.asset_demands import *
from functions.ex_agent_asset_demands import *
from functions.balance_sheet_adjustments import *
from functions.initialisation import *
from functions.market_mechanism import *
from functions.payouts_and_share_value import *
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

    #TODO calculate news process

    for day in range(environment.par.global_parameters["days"]-1):
        # initialise intraday prices at current price
        prices_tau = {portfolio: portfolio.var.price for portfolio in portfolios}
        
        for tau in range(100): #TODO this needs to be rewritten into a while loop when stopping criteria are defined
            
            for fund in funds:
                # 1 Expectation formation
                fund.hypothetical_returns = hypothetical_asset_returns(fund, prices_tau, environment.var.fx_rates)


                # update the value of redeemable shares and payouts to share holders
                fund.var.redeemable_shares, fund.var.payouts = payouts_and_share_value(portfolios, currencies, fund, environment)
                
                #fund.expected_vars = update_expectations(fund, assets, assets.exchange_rate, tau)
                
                # compute the weights of optimal balance sheet positions
                fund.var.weights = portfolio_optimization(fund) 
                
    
                # compute demand for balance sheet positions
                fund.var.asset_demand, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment)

    
            for ex in exogeneous_agents:
                exogeneous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogeneous_agents, portfolios )

            
            for a in portfolios:
                a.var.price = price_adjustment(portfolios, currencies, environment, exogeneous_agents , funds, a)
                        
            environment.var.fx_rates = fx_adjustment(portfolios, currencies, environment, exogeneous_agents , funds) 
            
        #this is where intraday calculations end
        #for fund in funds:
            #fund.var.asset, fund.var.cash = balance_sheet_adjustment(funds, portfolios, currencies, exogeneous_agents)
        
      

