def ex_agent_asset_demand(ex, exogeneous_agents, portfolios ):
    """
    Compute demand for three types of exogeneous agents, the underwriter, central bank, and fx interventionalist
    :param ex: String type of agent
    :param exogeneous_agents: list of exogeneous agents
    :param portfolios:  list of portfolio objects
    :return: demand for the exogeneous agents in question.
    """
    a_demand = {}
    
    for a in portfolios:
        out = a.par.maturity * (1-a.var.default_rate)
        mat = (1-a.par.maturity) * (1-a.var.default_rate)
        if ex == "underwriter":
            a_demand[a] = -(out * exogeneous_agents[ex].var_previous.assets[a] + (mat + a.var.default_rate) * a.par.quantity)
            
        if ex == "central_bank_domestic":
            a_demand[a] = exogeneous_agents[ex].var.asset_target[a] - out * exogeneous_agents[ex].var_previous.assets[a]

        if ex == "fx_interventionist" :
            a_demand[a] = 0
       
    return a_demand
