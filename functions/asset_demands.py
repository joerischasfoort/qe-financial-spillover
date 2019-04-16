from __future__ import division


def asset_demand(fund, portfolios, currencies, environment):
    """
    Calculate the asset and currency demand for a fund.
    :param fund: fund Object
    :param portfolios: list of portfolio objects
    :param currencies: list of currency objects
    :param environment: object containing parameters.
    :return:
    """
    a_demand = {} 
    for a in portfolios:       
        out = a.par.maturity * (1 - a.var.default_rate)

        a_demand[a] = ((fund.var.weights[a] * fund.var.redeemable_shares) / (environment.var.fx_rates.loc[fund.par.country,a.par.country] * a.var.price)) - out * fund.var_previous.assets[a]
        
    c_demand = {}   
    for c in currencies:  #   
        c_demand[c] = ((fund.var.weights[c] * fund.var.redeemable_shares) / environment.var.fx_rates.loc[fund.par.country,c.par.country] ) - fund.var.currency_inventory[c]
            
    return a_demand, c_demand


def asset_demand_oc(fund, portfolios, currencies, day):
    """
    Calculate the asset and currency demand for a fund for the one country model
    :param fund: fund Object
    :param portfolios: list of portfolio objects
    :param currencies: list of currency objects
    :param environment: object containing parameters.
    :return:
    """
    a_demand = {}
    for a in portfolios:
        out = a.par.maturity * (1 - a.var.default_rate[day])

        a_demand[a] = ((fund.var.weights[a] * fund.var.redeemable_shares[day]) / (a.var.price[day])) - out * fund.var.assets[a][day - 1] #TODO is this correct?

    c_demand = {}
    for c in currencies:  #
        c_demand[c] = (fund.var.weights[c] * fund.var.redeemable_shares[day]) - fund.var.currency_inventory[c]

    return a_demand, c_demand


def cash_inventory(fund, portfolios, currencies):
    cash_inv = {}
    for c in currencies:
        cash_inv[c] = fund.var_previous.currency[c] * (1 + c.par.nominal_interest_rate)
        
        for a in portfolios:
            if a.par.country == c.par.country:
                mat = (1-a.par.maturity) * (1 - a.var.default_rate)
                all = (1 - a.var.default_rate)
                cash_inv[c] = cash_inv[c] + (mat + all * a.par.nominal_interest_rate) * fund.var.assets[a] * a.par.face_value / a.par.quantity

        cash_inv[c] = cash_inv[c] - fund.var.payouts[c]
    
    return cash_inv


def cash_inventory_oc(fund, portfolios, currencies, day):
    cash_inv = {}
    for c in currencies:
        cash_inv[c] = fund.var.currency[c][day - 1] * (1 + c.par.nominal_interest_rate)

        for a in portfolios:
            mat = (1 - a.par.maturity) * (1 - a.var.default_rate[day])
            allo = (1 - a.var.default_rate[day])
            cash_inv[c] = cash_inv[c] + (mat + allo * a.par.nominal_interest_rate) * fund.var.assets[
                a][day - 1] * a.par.face_value / a.par.quantity #  TODO is this correct, day -1?

        cash_inv[c] = cash_inv[c] - fund.var.payouts

    return cash_inv
