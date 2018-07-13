from __future__ import division


def asset_demand(fund, portfolios, currencies, environment):
    
    
    a_demand = {} 
    for a in portfolios:       
        out = a.par.maturity * (1 - a.var.default_rate)

        a_demand[a] = ((fund.var.weights[a] * fund.var.redeemable_shares) / (environment.var.fx_rates.loc[fund.par.country,a.par.country] * a.var.price)) - out * fund.var_previous.assets[a]
        
    c_demand = {}   
    for c in currencies:  #   
        c_demand[c] = ((fund.var.weights[c] * fund.var.redeemable_shares) / environment.var.fx_rates.loc[fund.par.country,c.par.country] ) - fund.var.currency_inventory[c]
            
    return a_demand, c_demand


def cash_inventory(fund, portfolios, currencies):
    cash_inv = {}
    for c in currencies:
        cash_inv[c] = fund.var_previous.currency[c] * (1 + c.par.nominal_interest_rate)
        
        for a in portfolios:
            if a.par.country == c.par.country:
                mat= (1-a.par.maturity) * (1 - a.var.default_rate)
                all = (1 - a.var.default_rate)
                cash_inv[c] = cash_inv[c] + (mat + all * a.par.nominal_interest_rate) * fund.var.assets[a] * a.par.face_value / a.par.quantity
                

        cash_inv[c] = cash_inv[c] - fund.var.payouts[c]
    
    return cash_inv