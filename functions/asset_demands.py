from __future__ import division


def asset_demand(fund, portfolios, currencies, environment, tau, day):
    
    aux = {}
    
    a_demand = {}
    
    cash_from_matured_assets = {c:0 for c in currencies} #when assets mature, the principal is payed out in cash; this is reset to 0 every time the function is called
     
    for a in portfolios:
        
        out = a.par.maturity * (1 - a.var.default_rate)
        #Compute delta Q for domestic and foreign assets (equation 1.13 and 1.14); the correct relative exchange rate is accessed in the 
        #dataframe with row column (e.g. Xdf); 
        a_demand[a] = ((fund.var.weights[a] * fund.var.redeemable_shares) / (environment.var.fx_rates.loc[fund.par.country,a.par.country] * a.var.price)) - out * fund.var_previous.assets[a]
        
        # We compute what the funds received as cashflow from maturing fraction of bond portfolio
        aux[a] = (1-a.var.default_rate) * (1-a.par.maturity) *fund.var_previous.assets[a] * (a.par.face_value / a.par.quantity)
        for c in currencies:
            
            # for domestic assets
            if a.par.country == c.par.country:
                cash_from_matured_assets[c] = cash_from_matured_assets[c] + aux[a]
             # for foreign assets
        
 
    c_demand = {}
    
    for c in currencies:  #
        
        # In the demand for domestic cash one needs to take into account the payouts to shareholders in domestic currency
        
        if c.par.country == fund.par.country:
            c_demand[c] = ((fund.var.weights[c] * fund.var.redeemable_shares) / environment.var.fx_rates.loc[fund.par.country,c.par.country] ) -  (fund.var_previous.currency[c] *   (1.0 +  c.par.nominal_interest_rate)  + cash_from_matured_assets[c]) - fund.var.payouts)
        
        c_demand[c] = ((fund.var.weights[c] * fund.var.redeemable_shares) / environment.var.fx_rates.loc[fund.par.country,c.par.country] ) -  (fund.var_previous.currency[c] *   (1.0 +  c.par.nominal_interest_rate)  + cash_from_matured_assets[c])

    
    return a_demand, c_demand


