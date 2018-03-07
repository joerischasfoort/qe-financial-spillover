from __future__ import division


def balance_sheet_adjustments(fund,funds, portfolios, currencies, exogeneous_agents):
    
  
    #compute correcting factors for portfolios of assets
    pi = {}
    nu = {}
    new_position = {}
    for a in portfolios:
        set_of_positive = 0
        set_of_negative = 0
        for f in funds:
            if f.var.asset_demand[a] > 0:
                set_of_positive = set_of_positive + f.var.asset_demand[a]
            if f.var.asset_demand[a] < 0:
                set_of_negative = set_of_negative + f.var.asset_demand[a] # this will be a negative number
        excess_demand = set_of_positive - (- set_of_negative)
        
        if set_of_positive != 0:
            pi[a] = 1- (excess_demand / set_of_positive)
        else:
             pi[a] = 1
        if set_of_negative != 0:
            nu[a] = 1- (excess_demand / set_of_negative)
        else:
            nu[a] = 1
        
        #compute new balance sheet position
        if fund.var.asset_demand[a] > 0 and excess_demand > 0:
            new_position[a] = a.par.maturity * (1-a.var.default_rate) * fund.var_previous.assets[a] + fund.var.asset_demand[a] * pi[a]
            
        elif fund.var.asset_demand[a] < 0 and excess_demand < 0:
            new_position[a] = a.par.maturity * (1-a.var.default_rate) * fund.var_previous.assets[a] + fund.var.asset_demand[a] * nu[a]
        
        else :
            new_position[a] = a.par.maturity * (1-a.var.default_rate) * fund.var_previous.assets[a] + fund.var.asset_demand[a] 
     
        
        
    #compute correcting factors for portfolios of assets
    piC = {}
    nuC = {}
    new_cash_position = {}
    for c in currencies:
        set_of_positive = 0
        set_of_negative = 0
        for f in funds:
            if f.var.currency_demand[c] > 0:
                set_of_positive = set_of_positive + f.var.currency_demand[c]
            if f.var.currency_demand[c] < 0:
                set_of_negative = set_of_negative + f.var.currency_demand[c] # this will be a negative number
        excess_demand = set_of_positive - (- set_of_negative)
  
        if set_of_positive != 0:
            piC[c] = 1- (excess_demand / set_of_positive)
        else:
             piC[c] = 1
        if set_of_negative != 0:
            nuC[c] = 1- (excess_demand / set_of_negative)
        else:
            nuC[c] = 1
        #compute new balance sheet position

        if fund.var.currency_demand[c] > 0 and excess_demand > 0:
            new_cash_position[c] = fund.var_previous.currency[c] + fund.var.currency_demand[c] * piC[c]
            
        elif fund.var.currency_demand[c] < 0 and excess_demand < 0:
            new_cash_position[c] = fund.var_previous.currency[c] + fund.var.currency_demand[c] * nuC[c]
        
        else :
            new_cash_position[c] = fund.var_previous.currency[c] + fund.var.currency_demand[c] 
            

    
    return new_position, new_cash_position
        
        