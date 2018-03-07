from __future__ import division

def payouts_and_share_value(portfolios, currencies, fund, environment):
    payout = {}
    valuation_change = {}
    repayment_effect = {}
    price_effect = {}
    for a in portfolios:
        payout[a] = environment.var.fx_rates.loc[fund.par.country,a.par.country] * fund.var_previous.assets[a] * ((1-a.var.default_rate) * (a.par.face_value / a.par.quantity) * a.par.nominal_interest_rate - a.var.default_rate * a.var.price)
        repayment_effect[a] = (1-a.par.maturity) * (environment.var.fx_rates.loc[fund.par.country,a.par.country] * (a.par.face_value / a.par.quantity) - environment.var_previous.fx_rates.loc[fund.par.country,a.par.country] * a.var_previous.price)
        price_effect[a] = a.par.maturity * (environment.var.fx_rates.loc[fund.par.country,a.par.country] * a.var.price - environment.var_previous.fx_rates.loc[fund.par.country,a.par.country] * a.var_previous.price)
        valuation_change[a] = fund.var_previous.assets[a] * (1- a.var.default_rate) * (repayment_effect[a] + price_effect[a])
        
    for c in currencies:
        payout[c] = environment.var.fx_rates.loc[fund.par.country,c.par.country] * fund.var_previous.currency[c] * c.par.nominal_interest_rate
        valuation_change[c] = fund.var.currency[c] * (environment.var.fx_rates.loc[fund.par.country,c.par.country] - environment.var.fx_rates.loc[fund.par.country,c.par.country])
    

        
    redeemable_shares =  fund.var.redeemable_shares + sum(valuation_change.values())   
    
    return redeemable_shares, sum(payout.values())