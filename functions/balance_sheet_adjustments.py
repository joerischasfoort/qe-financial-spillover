from __future__ import division


def asset_excess_demand_and_correction_factors(fund,funds, portfolios, currencies, exogeneous_agents):
    
  
    #compute correcting factors for portfolios of assets
    pi = {}
    nu = {}
    excess_demand = {}

    for a in portfolios:
        set_of_positive = 0
        set_of_negative = 0
        
        for ex in exogeneous_agents:
            if exogeneous_agents[ex].var.asset_demand[a] > 0:
                set_of_positive = set_of_positive + exogeneous_agents[ex].var.asset_demand[a]           
            if exogeneous_agents[ex].var.asset_demand[a] < 0:
                set_of_negative = set_of_negative + exogeneous_agents[ex].var.asset_demand[a]
            
        for f in funds:
            if f.var.asset_demand[a] > 0:
                set_of_positive = set_of_positive + f.var.asset_demand[a]
            if f.var.asset_demand[a] < 0:
                set_of_negative = set_of_negative + f.var.asset_demand[a] # this will be a negative number
        
        excess_demand[a] = set_of_positive - (- set_of_negative)
        
        if set_of_positive != 0:
            pi[a] = 1- (excess_demand[a] / set_of_positive)
        else:
             pi[a] = 1
        if set_of_negative != 0:
            nu[a] = 1- (excess_demand[a] / set_of_negative)
        else:
            nu[a] = 1
        
        
    return excess_demand, pi, nu





def fund_asset_adjustments(fund, portfolios, excess_demand, pi, nu):
    new_position = {}
    for a in portfolios:
        #compute new balance sheet position of funds
        if fund.var.asset_demand[a] > 0 and excess_demand[a] > 0:
            new_position[a] = a.par.maturity * (1-a.var.default_rate) * fund.var_previous.assets[a] + fund.var.asset_demand[a] * pi[a]
            
        elif fund.var.asset_demand[a] < 0 and excess_demand[a] < 0:
            new_position[a] = a.par.maturity * (1-a.var.default_rate) * fund.var_previous.assets[a] + fund.var.asset_demand[a] * nu[a]
        
        else :
            new_position[a] = a.par.maturity * (1-a.var.default_rate) * fund.var_previous.assets[a] + fund.var.asset_demand[a] 
     
        
def ex_asset_adjustments(ex, portfolios, excess_demand, pi, nu):
    new_position = {}
    for a in portfolios:
        if ex == "central_bank_domestic":
            #compute new balance sheet position of exogenous agent
            if exogeneous_agents[ex].var.asset_demand[a] > 0 and excess_demand[a] > 0:
                new_position[a] = a.par.maturity * (1-a.var.default_rate) * exogeneous_agents[ex].var_previous.assets[a] + exogeneous_agents[ex].var.asset_demand[a] * pi[a]
                
            elif exogeneous_agents[ex].var.asset_demand[a] < 0 and excess_demand < 0:
                new_position[a] = a.par.maturity * (1-a.var.default_rate) * exogeneous_agents[ex].var_previous.assets[a] + exogeneous_agents[ex].var.asset_demand[a] * nu[a]
            
            else :
                new_position[a] = a.par.maturity * (1-a.var.default_rate) * exogeneous_agents[ex].var_previous.assets[a] + exogeneous_agents[ex].var.asset_demand[a]     
        
        if ex == "underwriter":
            #compute new balance sheet position of exogenous agent
            if  excess_demand < 0:
                new_position[a] = exogeneous_agents[ex].var.asset_demand[a] * (nu[a]-1)
            
            else :
                new_position[a] = 0  
     
        
        
        
def fund_cash_adjustments(fund,funds, portfolios, currencies, exogeneous_agents):
        
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
        
        