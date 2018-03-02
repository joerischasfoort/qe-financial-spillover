from __future__ import division


def asset_demand(fund, assets, cash):
    
    a_demand = {}
    
    for a in assets:
        a_demand[a] = ((fund.var.weights[a] * fund.var.redeemable_shares) / (fund.var.exchange_rate[a] * a.var.price)) - (1 - a.var.default_rate) * a.par.maturity * fund.var_previous.assets
    
    c_demand = {}
    
    for c in cash:
        c_demand[c] = ((fund.var.weights[a] * fund.var.redeemable_shares) / fund.var.exchange_rate[a] ) -  fund.var_previous.cash
        
    return  a_demand, c_demand
        