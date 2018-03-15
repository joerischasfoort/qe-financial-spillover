from __future__ import division


def asset_demand(fund, portfolios, currencies, environment):
    
    
    a_demand = {} 
    for a in portfolios:       
        out = a.par.maturity * (1 - a.var.default_rate)
        #Compute delta Q for domestic and foreign assets (equation 1.13 and 1.14); the correct relative exchange rate is accessed in the 
        #dataframe with row column (e.g. Xdf); 
        a_demand[a] = ((fund.var.weights[a] * fund.var.redeemable_shares) / (environment.var.fx_rates.loc[fund.par.country,a.par.country] * a.var.price)) - out * fund.var_previous.assets[a]
        

        
 
    c_demand = {}   
    for c in currencies:  #   
        c_demand[c] = ((fund.var.weights[c] * fund.var.redeemable_shares) / environment.var.fx_rates.loc[fund.par.country,c.par.country] ) - fund.var.cash_inventory[c]
        

    
    return a_demand, c_demand


def cash_inventory(fund, portfolios, currencies, environment):
    