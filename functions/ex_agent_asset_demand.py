def ex_agent_asset_demand(ex, exogeneous_agents, portfolios ):
    
    if ex == "underwriter":
        a_demand = {}
        for a in portfolios:
            a_demand[a]=-(a.par.maturity * (1-a.var.default_rate) * exogeneous_agents[ex].var_previous.assets[a] + ((1-a.par.maturity) * (1-a.var.default_rate) + a.var.default_rate) * a.par.quantity) 
        
        
        
    if ex == "central_bank_domestic":
        a_demand = {}
        for a in portfolios:
            a_demand[a]=exogeneous_agents[ex].var.asset_target[a] - a.par.maturity * (1-a.var.default_rate) * exogeneous_agents[ex].var_previous.assets[a]
    
    
    return a_demand