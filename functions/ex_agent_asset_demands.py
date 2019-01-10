def ex_agent_asset_demand(ex, exogenous_agents, portfolios):
    
    a_demand = {}
    
    for a in portfolios:
        out = a.par.maturity * (1-a.var.default_rate)
        mat = (1-a.par.maturity) * (1-a.var.default_rate)
        if ex == "underwriter":
            a_demand[a] =- (out * exogenous_agents[ex].var_previous.assets[a] + (mat + a.var.default_rate) * a.par.quantity)
            
        if ex == "central_bank_domestic":
            a_demand[a] = exogenous_agents[ex].var.asset_target[a] - out * exogenous_agents[ex].var_previous.assets[a]

        if ex == "fx_interventionist":
            a_demand[a] = 0
       
    return a_demand
