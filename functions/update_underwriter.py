from __future__ import division

def update_underwriter(assets, funds):
    underwriter_inventory = {}
    for a in portfolios:
        aux = 0
        for f in funds:
            aux=aux + f.var.assets[a]
            
        underwriter_inventory[a] = (1-a.par.maturity+a.var.default_rate) * a.par.quantity + (a.par.quantity - aux)
    
    return underwriter_inventory
    