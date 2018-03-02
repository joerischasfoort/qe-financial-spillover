from __future__ import division

def update_underwriter(assets, funds):
    underwriter_inventory = {}
    for a in assets:
        aux = 0
        for f in funds:
            aux=aux+f.var.assets
            
        underwriter_inventory[a] = (1-a.par.maturity+a.var.default_rate) * a.par.quantity + (a.par.quantity - aux)
    
    return underwriter_inventory
    