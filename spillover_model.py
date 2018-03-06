"""Main model"""
import numpy as np
import random

from functions.port_opt import *
from functions.asset_demand import *
from functions.balance_sheet_adjustments import *
from functions.initialisation import * 
from functions.market_mechanism import * 

def spillover_model(assets, cash, funds, days, seed):
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

    for day in range(days-1):
        
        for tau in range(100): #this needs to be rewritten into a while loop when stopping criteria are defined
            
            for fund in funds:
                # update the value of redeemable shares and payouts to share holders
                fund.var.redeemable_shares, fund.var.payouts = payouts_and_share_value(assets, currencies, fund)
                
                #fund.expected_vars = update_expectations(fund, assets, assets.exchange_rate, tau)
                
                # compute the weights of optimal balance sheet positions
                fund.var.weights = portfolio_optimization(fund) 
                
    
                # compute demand for balance sheet positions
                fund.var.asset_demand, fund.var.cash_demand = asset_demand(fund, assets, currencies)
    
                
            #Price adjustment
            assets.var.price = price_adjustment(funds, portfolios, exogenous_agents, p_change_intensity)
      
        #this is where intraday calculations end
        for fund in funds:
            fund.var.asset, fund.var.cash = balance_sheet_adjustments(fund, funds, portfolios, currencies)            
        
        underwriter.inventory = update_underwriter(assets, funds)    

