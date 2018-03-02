from __future__ import division


def balance_sheet_adjustments(fund,funds, assets, currencies):
    
  
    #compute correcting factors for portfolios of assets
    pi = {}
    nu = {}
    for a in assets:
        set_of_positive = 0
        set_of_negative = 0
        for f in funds:
            if f.var.asset_demand[a] > 0:
                set_of_positive = set_of_positive + f.var.asset_demand[a]
            if f.var.asset_demand[a] < 0:
                set_of_negative = set_of_negative + f.var.asset_demand[a] # this will be a negative number
        excess_demand = set_of_positive - (- set_of_negative)
        pi[a] = 1- (excess_demand / set_of_positive)
        nu[a] = 1- (excess_demand / set_of_negative)
        
        #compute new balance sheet position
        new_position = {}
        if fund.var.asset_demand[a] > 0 and excess_demand > 0:
            new_position[a] = assets[a].par.maturity * fund.var_previous.assets[a] + fund.var.asset_demand[a] * pi[a]
            
        elif fund.var.asset_demand[a] < 0 and excess_demand < 0:
            new_position[a] = assets[a].par.maturity * fund.var_previous.assets[a] + fund.var.asset_demand[a] * nu[a]
        
        else :
            new_position[a] = assets[a].par.maturity * fund.var_previous.assets[a] + fund.var.asset_demand[a] 
     
        
        
    #compute correcting factors for portfolios of assets
    piC = {}
    nuC = {}
    for c in currencies:
        set_of_positive = 0
        set_of_negative = 0
        for f in funds:
            if f.var.cash_demand[c] > 0:
                set_of_positive = set_of_positive + f.var.cash_demand[c]
            if f.var.cash_demand[c] < 0:
                set_of_negative = set_of_negative + f.var.cash_demand[c] # this will be a negative number
        excess_demand = set_of_positive - (- set_of_negative)
        piC[c] = 1- (excess_demand / set_of_positive)
        nuC[c] = 1- (excess_demand / set_of_negative)
        
        #compute new balance sheet position
        new_cash_position = {}
        if fund.var.cash_demand[c] > 0 and excess_demand > 0:
            new_cash_position[c] = fund.var_previous.cash[c] + fund.var.cash_demand[c] * piC[c]
            
        elif fund.var.cash_demand[c] < 0 and excess_demand < 0:
            new_cash_position[c] = fund.var_previous.cash[c] + fund.var.cash_demand[c] * nuC[c]
        
        else :
            new_cash_position[c] = fund.var_previous.cash[c] + fund.var.cash_demand[c] 
    
    return new_position, new_cash_position
        
        