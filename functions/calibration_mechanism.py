from __future__ import division
from math import log
from math import exp
import numpy as np

def update_RA_and_fx(portfolios, environment,currencies, funds,exogeneous_agents, var, var_original):
    Delta_RA = {}
    Delta_Demand = {}
    Delta_Capital = {}


    for a in np.random.permutation(portfolios):
        if a in var:
            a.par.nominal_interest_rate, delta_demand = interest_rate_adjustment(portfolios, exogeneous_agents, funds, a, a.par.cal_change_intensity)  # TODO: is the Delta_str really necessary?
            Delta_Demand.update({a: delta_demand})
        else:
            a.par.nominal_interest_rate, delta_demand = interest_rate_adjustment(portfolios, exogeneous_agents, funds, a, 0)  # TODO: is the Delta_str really necessary?
            Delta_Demand.update({a: delta_demand})



    for f in np.random.permutation(funds):
        for a in np.random.permutation(portfolios):
            if str(f)+"_"+str(a) in var:
                f.par.RA_matrix, delta_ra =  RA_matrix_adjustment(portfolios, currencies, a, f,  f.par.cal_change_intensity[a])
                Delta_RA.update({str(f)+"_"+str(a): delta_ra})
            elif str(f)+"_"+str(a) in var_original:
                f.par.RA_matrix, delta_ra = RA_matrix_adjustment(portfolios, currencies, a, f, 0)
                Delta_RA.update({str(f) + "_" + str(a): delta_ra})


        environment.var.fx_rates, Delta_Capital = fx_adjustment(portfolios, currencies, environment, funds,
                                                                0)

    if "FX" in var:
        environment.var.fx_rates, Delta_Capital = fx_adjustment(portfolios, currencies, environment, funds,
                                                                environment.par.global_parameters[
                                                                    "fx_change_intensity"])




    Deltas = {}
    Deltas.update(Delta_RA)
    Deltas.update(Delta_Demand)
    Deltas.update({"FX": Delta_Capital})


    return funds, environment, portfolios, Deltas




def RA_matrix_adjustment(portfolios, currencies, asset, fund,  adjustment_intensity):
    """
    Find the next  price of asset a.
    Sums over all demands of funds and exogenous agents
    and calculates the new price in tau via a log impact function
    """
    # Equation 1.18 : Get aggregate demand over all funds and exogenous agents
    demand = fund.var.asset_demand[asset]

    total_assets = fund.var.assets[asset]#sum(fund.var.assets[a] for a in portfolios)


    risk_aversion_mat = fund.par.RA_matrix.copy()



    risk_aversion_mat.loc[asset][asset]=max(1,exp(log(fund.par.RA_matrix.loc[asset][asset]) + adjustment_intensity * demand / total_assets))
    Delta = demand / total_assets

    for c in currencies:
        if c.par.country=='domestic':
            risk_aversion_mat.loc[c][c] =  risk_aversion_mat.loc[portfolios[0]][portfolios[0]]
        if c.par.country == 'foreign':
            risk_aversion_mat.loc[c][c] = risk_aversion_mat.loc[portfolios[2]][portfolios[2]]


    for row in risk_aversion_mat.index:
        for col in risk_aversion_mat.columns:
            risk_aversion_mat.loc[row, col] = np.sqrt(risk_aversion_mat.loc[row, row]) * np.sqrt(
                risk_aversion_mat.loc[col, col])


    return risk_aversion_mat, Delta




def interest_rate_adjustment(portfolios, exogeneous_agents, funds, a, adjustment_intensity):

    total_demand = {i: 0 for i in portfolios}

    total_demand_exogenous_agents = {i: 0 for i in portfolios}


    for ex in exogeneous_agents:
        total_demand_exogenous_agents[a] += exogeneous_agents[ex].var.asset_demand[a]

    # collect total demand from agents per asset
    for fund in funds:
        total_demand[a] += fund.var.asset_demand[a]

    # exit the fund loop and take into account underwriter and central bank demand
    total_demand[a] = total_demand[a] + total_demand_exogenous_agents[a]

    # Equation 1.17 : price adjustment
    log_new_interest = log(a.par.nominal_interest_rate) - adjustment_intensity * total_demand[a] / sum(i.par.quantity for i in portfolios)

    interest_rate = exp(log_new_interest)

    Delta_Demand = total_demand[a] / a.par.quantity

    # print "Price:", a, price, total_demand[a]/a.par.quantity

    return interest_rate,  Delta_Demand








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
            fund.var.aux_cash_dem = {c:0 for c in currencies}



        for fund in funds:
            red_share_fx_corr[fund] = fund.var.redeemable_shares * environment.var.fx_rates.loc[el[0], fund.par.country]
            for a in portfolios:
                if a.par.country != fund.par.country and fund.par.country == el[0]:
                    capital_DF = capital_DF + fund.var.asset_demand[a] * a.var.price * environment.var.fx_rates.loc[ el[0], el[1]]
                if a.par.country != fund.par.country and fund.par.country == el[1]:
                    capital_FD = capital_FD + fund.var.asset_demand[a] * a.var.price
                for c in currencies:
                    if a.par.country == c.par.country:
                        fund.var.aux_cash_dem[c]=fund.var.aux_cash_dem[c]-fund.var.asset_demand[a] * a.var.price
            for c in currencies:
                if c.par.country != fund.par.country and fund.par.country == el[0]:
                    capital_DF = capital_DF + fund.var.currency_demand[c] * environment.var.fx_rates.loc[el[0], el[1]]
                if c.par.country != fund.par.country and fund.par.country == el[1]:
                    capital_FD = capital_FD + fund.var.currency_demand[c]
                fund.var.aux_cash_dem[c] = fund.var.aux_cash_dem[c] + fund.var.currency_demand[c]

        #capital_df = 0
        #capital_fd = 0
        #for fund in funds:
        #    for c in currencies:
        #        if fund.par.country != c.par.country and fund.par.country == el[0]:
        #            capital_df = capital_df + fund.var.aux_cash_dem[c]* environment.var.fx_rates.loc[el[0], el[1]]
        #        if fund.par.country != c.par.country and fund.par.country == el[1]:
        #            capital_fd = capital_fd + fund.var.aux_cash_dem[c]

        Delta_Capital = (capital_DF - capital_FD ) / sum(red_share_fx_corr.values())
        #Delta_capital =(capital_df - capital_fd ) / sum(red_share_fx_corr.values())


        log_new_fx_rate = log(environment.var.fx_rates.loc[el[0]][el[1]]) + adjustment_intensity * Delta_Capital

        fx_rate = exp(log_new_fx_rate)

        environment.var.fx_rates.loc[el[0]][el[1]] = fx_rate
        environment.var.fx_rates.loc[el[1]][el[0]] = 1 / fx_rate

        # print "testing", fx_rate, Delta_Capital
        # print "FX:", fx_rate, Delta_Capital

    return environment.var.fx_rates, Delta_Capital



def   I_intensity_parameter_adjustment_cal(jump_counter, no_jump_counter, test_sign, Deltas, environment, portfolios, funds, var):

    portfolios_str = [str(a) for a in portfolios]
    funds_str = [str(f) for f in funds]

    jc = 10 # jumps until intensity is adjusted
    nojc = 20 # consecutive non-jumps until intensity is adjusted
    test = {}
    jump = {x:0 for x in jump_counter}
    no_jump = {x:0 for x in jump_counter}

    for i in jump_counter:

        if i in portfolios:
            change_intensity = i.par.cal_change_intensity
        if isinstance(i,str) and i!="FX":
            f_str = i.split("_")[0]
            a_str = i.split("_")[1]

            fund = funds[funds_str.index(f_str)]
            asset = portfolios[portfolios_str.index(a_str)]
            change_intensity = fund.par.cal_change_intensity[asset]

        test[i] = test_sign[i] / np.sign(Deltas[i])
        test_sign[i] = np.sign(Deltas[i])

        if test[i] == -1:
            jump[i] = 1
        if test[i] == 1:
            no_jump[i] = 1


        if len(var)==1:
            if sum(jump[i] for i in jump)>0 and i in var:
                jump_counter[i] += 1
                no_jump_counter[i] = 0
            if sum(jump[i] for i in jump) == 0 and i in var:
                no_jump_counter[i] += 1
                jump_counter[i] = 0

        else:
            if jump[i] == 1 and i in var:# and convergence[i] == False:
                jump_counter[i] += 1
                no_jump_counter[i] = 0

            if no_jump[i] == 1 and i in var:# and convergence[i] == False:
                no_jump_counter[i] += 1




        if jump_counter[i] > jc and i!="FX" and i in var:# and convergence[i] == False:
            change_intensity = change_intensity  / 3
            jump_counter[i] = 0
            no_jump_counter[i]=0


        if jump_counter[i] > jc and i == "FX" and i in var:# and convergence[i] == False:
            environment.par.global_parameters['fx_change_intensity'] = environment.par.global_parameters['fx_change_intensity'] / 3
            jump_counter[i] = 0
            no_jump_counter[i]=0


        if no_jump_counter[i] > nojc and i!="FX" and i in var:# and convergence[i] == False:
            change_intensity =  min(0.1, change_intensity * 1.1)
            no_jump_counter[i] = 0
            jump_counter[i] = 0


        if no_jump_counter[i] > nojc and i=="FX" and i in var:# and convergence[i] == False:
            environment.par.global_parameters['fx_change_intensity'] = min(0.1, environment.par.global_parameters['fx_change_intensity'] * 1.1)
            no_jump_counter[i] = 0
            jump_counter[i] = 0

        if i in portfolios:
            i.par.cal_change_intensity = change_intensity

        if isinstance(i, str) and i != "FX":
            fund.par.cal_change_intensity[asset] = change_intensity


    return  jump_counter, no_jump_counter, test_sign, environment



def check_convergence_cal(Deltas, conv_bound, tau):
    convergence_bound = {i: conv_bound for i in Deltas}

    convergence_condition = {i: abs(Deltas[i]) < convergence_bound[i] for i in Deltas}
    convergence = sum(convergence_condition[i] for i in convergence_condition) == len(Deltas) and tau > 20

    if tau > 2000: convergence = True  # exit iteration after many iterations

    return convergence, convergence_condition