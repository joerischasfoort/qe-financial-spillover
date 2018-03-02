from __future__ import division


def asset_demand(fund, portfolios, currencies):
    
    a_demand = {}
    
    for a in portfolios:
        a_demand[a] = ((fund.var.weights[a] * fund.var.redeemable_shares) / (fund.var.exchange_rate[a] * a.var.price)) - (1 - a.var.default_rate) * a.par.maturity * fund.var_previous.assets[a]
    
    c_demand = {}
    
    for c in currencies:
        c_demand[c] = ((fund.var.weights[c] * fund.var.redeemable_shares) / fund.var.exchange_rate[c] ) -  fund.var_previous.currency[c]
        
    return  a_demand, c_demand
        