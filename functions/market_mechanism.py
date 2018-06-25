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


def price_adjustment(portfolios, environment, exogeneous_agents, funds, a, adjustment_intensity):
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
    log_new_price = log(a.var.price) + adjustment_intensity * total_demand[a] / a.par.quantity


    price = exp(log_new_price)

    Delta_Demand = total_demand[a] / a.par.quantity
    Delta_Demand_string = "Delta_"+ str(a)

    # print "Price:", a, price, total_demand[a]/a.par.quantity

    return price, Delta_Demand_string, Delta_Demand


def fx_adjustment(portfolios, currencies, environment, funds, adjustment_intensity):
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

    for el in combinations:


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



        Delta_Capital = (capital_DF - capital_FD ) / sum(red_share_fx_corr.values())


        log_new_fx_rate = log(environment.var.fx_rates.loc[el[0]][el[1]]) + adjustment_intensity * Delta_Capital

        fx_rate = exp(log_new_fx_rate)

        environment.var.fx_rates.loc[el[0]][el[1]] = fx_rate
        environment.var.fx_rates.loc[el[1]][el[0]] = 1 / fx_rate

        # print "testing", fx_rate, Delta_Capital
        # print "FX:", fx_rate, Delta_Capital

    return environment.var.fx_rates, Delta_Capital



def I_intensity_parameter_adjustment(jump_counter, no_jump_counter, test_sign, Deltas, environment, convergence_bound, var):
    jc = 10 # jumps until intensity is adjusted
    nojc = 10 # consecutive non-jumps until intensity is adjusted
    test = {}
    jump = {x:0 for x in jump_counter}
    no_jump = {x:0 for x in jump_counter}
    #convergence = {}
    for i in jump_counter:
        test[i] = test_sign[i] / np.sign(Deltas[i])
        test_sign[i] = np.sign(Deltas[i])

        #convergence[i]=abs(Deltas[i]) < convergence_bound

        if test[i] == -1:
            jump[i] = 1
        if test[i] == 1:
            no_jump[i] = 1

        if jump[i] == 1 and i in var:
            jump_counter[i] += 1
            no_jump_counter[i] = 0

        if no_jump[i] == 1 and i in var:
            no_jump_counter[i] += 1

        if jump_counter[i] > jc and i!="FX" and i in var:# and convergence[i] == False:
            i.par.change_intensity = i.par.change_intensity  / 2
            jump_counter[i] = 0
            no_jump_counter[i]=0


        if jump_counter[i] > jc and i == "FX" and i in var :#and convergence[i] == False:
            environment.par.global_parameters['fx_change_intensity'] = environment.par.global_parameters['fx_change_intensity'] / 2
            jump_counter[i] = 0
            no_jump_counter[i]=0


        if no_jump_counter[i] > nojc and i!="FX" and i in var:# and convergence[i] == False:
            i.par.change_intensity =  min(0.1, i.par.change_intensity * 1.1)
            no_jump_counter[i] = 0
            jump_counter[i] = 0


        if no_jump_counter[i] > nojc and i=="FX" and i in var:# and convergence[i] == False:
            environment.par.global_parameters['fx_change_intensity'] = min(0.1, environment.par.global_parameters['fx_change_intensity'] * 1.1)
            no_jump_counter[i] = 0
            jump_counter[i] = 0


    return  jump_counter, no_jump_counter, test_sign, environment



