"""Main model"""
import numpy as np
import random

from functions.port_opt import *
from functions.initialisation import * 

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
        tau = 0
        for fund in funds:
            #fund.expected_vars = update_expectations(fund, assets, assets.exchange_rate, tau)
            
            # compute the weights of optimal balance sheet positions
            fund.var.weights = portfolio_optimization(fund) 
            

            #New demands 
            #fund.var.demands = new_demand(fund)
            
            #Market mechanism  
            #assets.var.price = lazy_wal_auction(assets, funds, imperfection_tolerance, gamma)
              
            
            
            
>>>>>>> 22f9c767fca44ac23f6099a0db1c69c5490253be
