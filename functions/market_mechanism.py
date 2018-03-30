from __future__ import division

from math import log
from math import exp
import numpy as np


def convert_P2R(a, price):
    mat = (1 - a.par.maturity) * (1 - a.var.default_rate)
    alla = (1 - a.var.default_rate)
    ret = ((a.par.face_value / a.par.quantity) * (
                mat + a.par.nominal_interest_rate * alla) / price) - a.var.default_rate - mat
    return ret


def convert_R2P(a, ret):
    mat = (1 - a.par.maturity) * (1 - a.var.default_rate)
    alla = (1 - a.var.default_rate)
    price = ((a.par.face_value / a.par.quantity) * (mat + a.par.nominal_interest_rate * alla)) / (ret + a.var.default_rate + mat)
    return price


def price_adjustment(portfolios, environment, exogeneous_agents, funds, a):
    """
    Find the next  price of asset a.
    Sums over all demands of funds and exogenous agents
    and calculates the new price in tau via a log impact function
    """
    # Equation 1.18 : Get aggregate demand over all funds and exogenous agents
    total_demand = {i: 0 for i in portfolios}

    total_demand_exogenous_agents = {i: 0 for i in portfolios}
    # first loop over all exogenous agents and collect their demand per asset

    for ex in exogeneous_agents:
        total_demand_exogenous_agents[a] += exogeneous_agents[ex].var.asset_demand[a]

    # collect total demand from agents per asset
    for fund in funds:
        total_demand[a] += fund.var.asset_demand[a]

    # exit the fund loop and take into account underwriter and central bank demand
    total_demand[a] = total_demand[a] + total_demand_exogenous_agents[a]
    # print a.var.price, total_demand[a]

    # Equation 1.17 : price adjustment
    log_new_price = log(a.var.price) + environment.par.global_parameters['p_change_intensity'] * total_demand[a] / a.par.quantity

    log_new_ret = log(a.var.aux_ret) - environment.par.global_parameters['p_change_intensity'] * total_demand[a] / a.par.quantity

    price = convert_R2P(a, exp(log_new_ret))

    Delta_Demand = total_demand[a] / a.par.quantity

    # print "Price:", a, price, total_demand[a]/a.par.quantity

    return price, exp(log_new_ret), Delta_Demand


def fx_adjustment(portfolios, currencies, environment, exogeneous_agents, funds, noise):
    """
    Find the new fxrate
    """

    # We iterate over the  exchange rate matrix to get all
    # possible combinations of "from_country" "to_country"
    # then calculate the new exchange rate for every exchange rate pair above the diagonal

    # Make a list of combinations
    combinations = []

    for column in range(len(environment.var.fx_rates.index)):
        row = 0

    while row < column:
        combination_tuple = (environment.var.fx_rates.index[row], environment.var.fx_rates.columns[column])
        row = row + 1
        combinations.append(combination_tuple)

    K_delta = 0  # net capital flows
    fx_rate = 0

    for el in combinations:

        weight_f = 0  # This is the sum of   weights per fund DEMANDING a currency (the first sum in equation 1.23)
        aux = 0  # helper variable

        weight_fd = 0  # This is the sum of   weights per fund from the other perspective (the second term in the nominator term inequation 1.23 )
        aux_2 = 0  # helper variable

        tot_red_shares = 0

        red_share_fx_corr={}

        capital_DF = 0
        capital_FD = 0

        for fund in funds:
            red_share_fx_corr[fund] = fund.var.redeemable_shares * environment.var.fx_rates.loc[el[0], fund.par.country]
            for a in portfolios:
                if a.par.country != fund.par.country and fund.par.country == el[0]:
                    capital_DF = capital_DF + fund.var.asset_demand[a] * a.var.price * environment.var.fx_rates.loc[ el[0], el[1]]
                if a.par.country != fund.par.country and fund.par.country == el[1]:
                    capital_FD = capital_FD + fund.var.asset_demand[a] * a.var.price
            for c in currencies:
                if c.par.country != fund.par.country and fund.par.country == el[0]:
                    capital_DF = capital_DF + fund.var.currency_demand[c] * environment.var.fx_rates.loc[el[0], el[1]]
                if c.par.country != fund.par.country and fund.par.country == el[1]:
                    capital_FD = capital_FD + fund.var.currency_demand[c]



        Delta_Capital = noise + (capital_DF - capital_FD ) / sum(red_share_fx_corr.values())


        log_new_fx_rate = log(environment.var.fx_rates.loc[el[0]][el[1]]) + environment.par.global_parameters["fx_change_intensity"] * Delta_Capital

        fx_rate = exp(log_new_fx_rate)

        environment.var.fx_rates.loc[el[0]][el[1]] = fx_rate
        environment.var.fx_rates.loc[el[1]][el[0]] = 1 / fx_rate

        # print "testing", fx_rate, Delta_Capital
        # print "FX:", fx_rate, Delta_Capital

    return environment.var.fx_rates, Delta_Capital

