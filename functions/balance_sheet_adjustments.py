from __future__ import division

import numpy as np

    
    
def asset_excess_demand_and_correction_factors(funds, portfolios, currencies, exogeneous_agents):
      
    #compute correcting factors for portfolios of assets
    pi = {}
    nu = {}
    excess_demand = {}
    set_of_positive = {a:0 for a in portfolios}
    set_of_negative = {a:0 for a in portfolios}
    for a in portfolios:        
        for ex in exogeneous_agents:
            if exogeneous_agents[ex].var.asset_demand[a] > 0:
                set_of_positive[a] = set_of_positive[a] + exogeneous_agents[ex].var.asset_demand[a]
            if exogeneous_agents[ex].var.asset_demand[a] < 0:
                set_of_negative[a] = set_of_negative[a] + exogeneous_agents[ex].var.asset_demand[a]
            
        for f in funds:
            if f.var.asset_demand[a] > 0:
                set_of_positive[a] = set_of_positive[a] + f.var.asset_demand[a]
            if f.var.asset_demand[a] < 0:
                set_of_negative[a] = set_of_negative[a] + f.var.asset_demand[a] # this will be a negative number
        
        excess_demand[a] = set_of_positive[a] - (- set_of_negative[a])
        
        if set_of_positive[a] != 0:
            pi[a] = 1- (excess_demand[a] / set_of_positive[a])
        else:
             pi[a] = 1
        if set_of_negative[a] != 0:
            nu[a] = 1- (excess_demand[a] / set_of_negative[a])
        else:
            nu[a] = 1
        
        
    return excess_demand, pi, nu





def fund_asset_adjustments(fund, portfolios, excess_demand, pi, nu):
    
    new_position = {}
    for a in portfolios:
        out=a.par.maturity * (1-a.var.default_rate)
         
        #compute new balance sheet position of funds
        if fund.var.asset_demand[a] > 0 and excess_demand[a] > 0:
            new_position[a] = out * fund.var_previous.assets[a] + fund.var.asset_demand[a] * pi[a]
            
        elif fund.var.asset_demand[a] < 0 and excess_demand[a] < 0:
            new_position[a] = out * fund.var_previous.assets[a] + fund.var.asset_demand[a] * nu[a]
        
        else :
            new_position[a] = out * fund.var_previous.assets[a] + fund.var.asset_demand[a] 
    
    return new_position
        
def ex_asset_adjustments(ex, portfolios, excess_demand, pi, nu, exogeneous_agents):
    new_position = {}
    for a in portfolios:
        out=a.par.maturity * (1-a.var.default_rate)
        if ex == "central_bank_domestic":
            #compute new balance sheet position of exogenous agent
            if exogeneous_agents[ex].var.asset_demand[a] > 0 and excess_demand[a] > 0:
                new_position[a] = out * exogeneous_agents[ex].var_previous.assets[a] + exogeneous_agents[ex].var.asset_demand[a] * pi[a]
                
            elif exogeneous_agents[ex].var.asset_demand[a] < 0 and excess_demand[a] < 0:
                new_position[a] = out * exogeneous_agents[ex].var_previous.assets[a] + exogeneous_agents[ex].var.asset_demand[a] * nu[a]
            
            else :
                new_position[a] = out * exogeneous_agents[ex].var_previous.assets[a] + exogeneous_agents[ex].var.asset_demand[a]     
        
        if ex == "underwriter":
            #compute new balance sheet position of exogenous agent
            if  excess_demand[a] < 0:
                new_position[a] = exogeneous_agents[ex].var.asset_demand[a] * (nu[a]-1)
            
            else :
                new_position[a] = 0  
    
    return new_position
        
def cash_demand_correction(fund, currencies,environment):
    new_cash_demand={c:0 for c in currencies}
    for c, cu in zip(currencies, reversed(currencies)):
        if np.sign(fund.var.currency_demand[c])!=np.sign(fund.var.currency_demand[cu]):
            new_cash_demand[c]=np.sign(fund.var.currency_demand[c])*min(abs(fund.var.currency_demand[c]),abs(environment.var.fx_rates.loc[c.par.country,cu.par.country]*fund.var.currency_demand[cu]))
                    
    return new_cash_demand 
        
def cash_excess_demand_and_correction_factors(funds, currencies):

    #compute correcting factors for portfolios of assets
    piC = {}
    nuC = {}
    excess_demandC = {}
    set_of_positive = {c:0 for c in currencies}
    set_of_negative = {c:0 for c in currencies}
        
    for c in currencies:
        # computing excess cash demand for investor agents (independent)
        for f in funds:
            if f.var.currency_demand[c] > 0:
                set_of_positive[c] = set_of_positive[c] + f.var.currency_demand[c]
            if f.var.currency_demand[c] < 0:
                set_of_negative[c] = set_of_negative[c] + f.var.currency_demand[c] # this will be a negative number
  
            
        excess_demandC[c] = set_of_positive[c] - (- set_of_negative[c])
  
        if set_of_positive[c] != 0:
            piC[c] = 1- (excess_demandC[c] / set_of_positive[c])
        else:
             piC[c] = 1
        if set_of_negative[c] != 0:
            nuC[c] = 1- (excess_demandC[c] / set_of_negative[c])
        else:
            nuC[c] = 1
        #compute new balance sheet position
    return nuC, piC, excess_demandC


def fund_cash_adjustments(nuC, piC, excess_demandC, currencies, fund):
    new_cash_position = {}
    
    for c in currencies:    
        if fund.var.currency_demand[c] > 0 and excess_demandC[c] > 0:
            new_cash_position[c] = fund.var.currency_inventory[c] + fund.var.currency_demand[c] * piC[c]
            
        elif fund.var.currency_demand[c] < 0 and excess_demandC[c] < 0:
            new_cash_position[c] = fund.var.currency_inventory[c] + fund.var.currency_demand[c] * nuC[c]
        
        else:
            new_cash_position[c] = fund.var.currency_inventory[c] + fund.var.currency_demand[c] 
    

    return new_cash_position


def fund_cash_inventory_adjustment(fund, portfolios, currencies):
    net_cash_flows = {c:0 for c in currencies}
    new_cash_inventory = {}

    for c in currencies:
        for a in portfolios:
            if a.par.country == c.par.country:
                out = a.par.maturity * (1 - a.var.default_rate)
                net_cash_flows[c] = net_cash_flows[c] + (out * (fund.var_previous.assets[a]) - fund.var.assets[a]) * a.var.price

        new_cash_inventory[c] = fund.var.currency_inventory[c] + net_cash_flows[c]

    return new_cash_inventory



