from __future__ import division


def asset_demand(fund, portfolios, currencies):
    
    a_demand = {}
    cash_from_matured_assets = {c:0 for c in currencies}
    
    for a in portfolios:
        a_demand[a] = ((fund.var.weights[a] * fund.var.redeemable_shares) / (environment.var.fx_rates.loc[fund.par.country,a.par.country] * a.var.price)) - (1 - a.var.default_rate) * a.par.maturity * fund.var_previous.assets[a]
        if a.par.country ==
    c_demand = {}
    
    for c in currencies:
        c_demand[c] = ((fund.var.weights[c] * fund.var.redeemable_shares) / environment.var.fx_rates.loc[fund.par.country,c.par.country] ) -  (fund.var_previous.currency[c]+cash_from_matured_assets[c])
        
    return  a_demand, c_demand
    

    test = {}
    for a in portfolios:
        test[a] = (1-a.var.default_rate) * (1-a.par.maturity) *fund.var.assets[a] * (a.par.face_value / a.par.quantity)
    for (a,c) in (portfolios , currencies):
        if a.par.country == c.par.country:
            cash_from_matured_assets[c] = cash_from_matured_assets[c] + test[a]