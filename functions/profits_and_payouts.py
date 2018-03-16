from __future__ import division


def profit_and_payout(fund, assets, currencies, environment):
    
    profit_per_asset = {}
    total_profit = 0
    for a in assets:
    
        out = a.par.maturity * (1 - a.var.default_rate)
        mat = (1 - a.par.maturity) * (1 - a.var.default_rate)
        all = out + mat
        
        repayment_effect = mat * (environment.var.fx_rates.loc[fund.par.country, a.par.country] * a.par.face_value / a.par.quantity - environment.var_previous.fx_rates.loc[fund.par.country,a.par.country] * a.var_previous.price)
        
        price_effect = out * (environment.var.fx_rates.loc[fund.par.country, a.par.country] * a.var.price - environment.var_previous.fx_rates.loc[fund.par.country, a.par.country] * a.var_previous.price)
        
        interest_effect = all * environment.var.fx_rates.loc[fund.par.country, a.par.country] * a.par.face_value / a.par.quantity * a.par.nominal_interest_rate
        
        default_effect = a.var.default_rate * environment.var_previous.fx_rates.loc[fund.par.country, a.par.country] * a.var_previous.price
        
        profit_per_asset[a] = repayment_effect + price_effect + interest_effect - default_effect
        
        total_profit = total_profit + profit_per_asset[a] * fund.var.assets[a]
        
    for c in currencies:
        
        profit_per_asset[c] = c.par.nominal_interest_rate * environment.var.fx_rates.loc[fund.par.country, c.par.country] + environment.var.fx_rates.loc[fund.par.country, c.par.country] - environment.var_previous.fx_rates.loc[fund.par.country,c.par.country]
        
        total_profit = total_profit + profit_per_asset[c] * fund.var.currency[c]
        
    
    redeemable_shares = min(fund.var_previous.redeemable_shares + total_profit, fund.var.size_target)

    payouts = fund.var_previous.redeemable_shares + total_profit - redeemable_shares  
    
    return profit_per_asset, redeemable_shares, payouts
    