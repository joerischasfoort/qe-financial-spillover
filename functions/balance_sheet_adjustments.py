from __future__ import division

def balance_sheet_adjustment(funds, portfolios, currencies, exogeneous_agents):
    
    excess_demand, pi, nu = asset_excess_demand_and_correction_factors(funds, portfolios, currencies, exogeneous_agents)
    
    for fund in funds:
        fund.var.assets = fund_asset_adjustments(fund, portfolios, excess_demand, pi, nu)
    
    for ex in exogeneous_agents:
        exogeneous_agents[ex].var.assets = ex_asset_adjustments(ex, portfolios, excess_demand, pi, nu, exogeneous_agents)
    
    excess_demandC, piC, nuC = cash_excess_demand_and_correction_factors(funds, portfolios, currencies, exogeneous_agents)
    
    for fund in funds:
        fund.var.currencies = fund_cash_adjustments(nuC, piC, excess_demandC, currencies, fund, portfolios)

    
    
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
                set_of_positive = set_of_positive + exogeneous_agents[ex].var.asset_demand[a]           
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
        if set_of_negative != 0:
            nu[a] = 1- (excess_demand[a] / set_of_negative[a])
        else:
            nu[a] = 1
        
        
    return excess_demand, pi, nu





def fund_asset_adjustments(fund, portfolios, excess_demand, pi, nu):
    
    out=a.par.maturity * (1-a.var.default_rate)
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
        
        
        
def cash_excess_demand_and_correction_factors(funds, portfolios, currencies, exogeneous_agents):
                
    #computing cash supply (after asset transactions have been made) of exogenous agents
    cb_cash_supply={c:0 for c in currencies}
    underwriter_cash_supply={c:0 for c in currencies}
    for ex in exogeneous_agents:
        auxCB = {}
        auxU = {}
        for a in portfolios:
            out=a.par.maturity * (1-a.var.default_rate)    
            if ex == "central_bank_domestic":
                auxCB[a]=(exogeneous_agents[ex].var.assets[a]- out * exogeneous_agents[ex].var_previous.assets[a]) * a.var.price
                for c in currencies:
                    if exogeneous_agents[ex].par.country == a.par.country and a.par.country == c.par.country :
                        cb_cash_supply[c] = cb_cash_supply[c] + auxCB[a]

            if ex == "underwriter":
                auxU[a]=(exogeneous_agents[ex].var.assets[a] - (-exogeneous_agents[ex].var.asset_demand[a])) * a.var.price
                for c in currencies:
                    if a.par.country == c.par.country :
                        underwriter_cash_supply[c] = underwriter_cash_supply[c] + auxU[a]

        
    #compute correcting factors for portfolios of assets
    piC = {}
    nuC = {}
    excess_demandC = {}
    set_of_positive = {c:0 for c in currencies}
    set_of_negative = {c:0 for c in currencies}
        
    for c in currencies:
        if underwriter_cash_supply[c] > 0:
            set_of_positive[c] = set_of_positive[c] + underwriter_cash_supply[c]
        if underwriter_cash_supply[c] < 0:
            set_of_negative[c] = set_of_negative[c] + underwriter_cash_supply[c]
        if cb_cash_supply[c] > 0:
            set_of_positive[c] = set_of_positive[c] + cb_cash_supply[c]
        if cb_cash_supply[c] < 0:
            set_of_negative[c] = set_of_negative[c] + cb_cash_supply[c]


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



def fund_cash_adjustments(nuC, piC, excess_demandC, currencies, fund, portfolios):       
    new_cash_position = {}
    aux = {}
    
    for c in currencies:    
        if fund.var.currency_demand[c] > 0 and excess_demandC[c] > 0:
            new_cash_position[c] = fund.var.cash_inventory[c] + fund.var.currency_demand[c] * piC[c]
            
        elif fund.var.currency_demand[c] < 0 and excess_demandC[c] < 0:
            new_cash_position[c] = fund.var.cash_inventory[c] + fund.var.currency_demand[c] * nuC[c]
        
        else :
            new_cash_position[c] = fund.var.cash_inventory[c] + fund.var.currency_demand[c] 
            print fund.var.currency_demand[c], fund.var.weights[c], fund.var_previous.currency[c] + cash_from_matured_assets[c]
    
    
    return new_cash_position
        
        