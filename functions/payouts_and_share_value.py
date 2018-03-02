from __future__ import division

def payouts_and_share_value(assets, currencies, fund):
    payout = {}
    valuation_change = {}
    repayment_effect = {}
    price_effect = {}
    for a in assets:
        payout[a] = fund.var.exchange_rate[a] * fund.var_previous.assets[a] * ((1-a.var.default_rate) * (a.par.face_value / a.par.quantity) * a.par.nominal_interest_rate - a.var.default_rate * a.var.price)
        repayment_effect[a] = (1-a.par.maturity) * (fund.var.exchange_rate[a] * (a.par.face_value / a.par.quantity) - fund.var_previous.exchange_rate[a] * a.var_previous.price)
        price_effect[a] = a.par.maturity * (fund.var.exchange_rate[a] * a.var.price - fund.var_previous.exchange_rate[a] * a.var_previous.price)
        valuation_change[a] = fund.var_previous.asset[a] * (1- a.var.default_rate) * (repayment_effect[a] + price_effect[a])
        
    for c in currencies:
        payout[c] = fund.var.exchange_rate[c] * fund.var_previous.cash[c] * c.par.interest_rate
        valuation_change[c] = fund.var.cash[c] * (fund.var.exchange_rate[c] - fund.var_previous.exchange_rate[c])
    

        
    redeemable_shares =  fund.var.redeemable_shares + sum(valuation_change.values())   
    
    return redeemable_shares, sum(payout.values())