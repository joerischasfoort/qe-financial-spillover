#!/usr/bin/env python2
# -*- coding: utf-8 -*-

def show_fund(fund, portfolios, currencies, environment):
    
    print("Balance sheet Fund" , fund.name)
    print("-------------------------")
    sum_asset =0
    for a in portfolios:
        sum_asset += fund.var.assets[a] * a.var.price * environment.var.fx_rates.loc[fund.par.country][a.par.country]
    
        print(a, fund.var.assets[a] , "Price: ", a.var.price, "Fx rate:", environment.var.fx_rates.loc[fund.par.country][a.par.country]) 
    
    for c in currencies:
        sum_asset += fund.var.currency[c] * environment.var.fx_rates.loc[fund.par.country][c.par.country]
    
        print(c, fund.var.currency[c] , "Fx rate:", environment.var.fx_rates.loc[fund.par.country][c.par.country]) 
    
    
    print("XXXXXX")
    print("SUM ASSET SIDE",sum_asset)  
    print("Redeemable Shares", fund.var.redeemable_shares)



