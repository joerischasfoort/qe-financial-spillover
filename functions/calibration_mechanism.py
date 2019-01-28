from __future__ import division
from math import log
from math import exp
import numpy as np
from calibration_functions import *

def update_RA_and_fx(portfolios, environment,currencies, funds,exogeneous_agents, var, var_original,U):
    Delta_RA = {}
    Delta_Demand = {}
    Delta_Capital = {}


   # for a in np.random.permutation(portfolios):
   #     if a in var:
   #         a.par.nominal_interest_rate, delta_demand = interest_rate_adjustment(portfolios, exogeneous_agents, funds, a, a.par.cal_change_intensity)  # TODO: is the Delta_str really necessary?
   #         Delta_Demand.update({a: delta_demand})
   #     else:
   #         a.par.nominal_interest_rate, delta_demand = interest_rate_adjustment(portfolios, exogeneous_agents, funds, a, 0)  # TODO: is the Delta_str really necessary?
   #         Delta_Demand.update({a: delta_demand})
   #

    for a in portfolios:
        if a in var:
            a.par.nominal_interest_rate, delta_demand = int_adjustment(funds, a, a.par.cal_change_intensity)  # TODO: is the Delta_str really necessary?
            Delta_Demand.update({a: delta_demand})
        else:
            a.par.nominal_interest_rate, delta_demand = int_adjustment(funds, a, 0)  # TODO: is the Delta_str really necessary?
            Delta_Demand.update({a: delta_demand})
        #print(delta_demand)
#    for c in currencies:
#        if c in var:
#            c.par.RA, delta_ra =  RA_matrix_adjustment_cash(funds, c, c.par.cal_change_intensity)
#            Delta_RA.update({c: delta_ra})
#        elif c in var_original:
#            c.par.RA, delta_ra =  RA_matrix_adjustment_cash(funds, c, 0)
#            Delta_RA.update({c: delta_ra})
#

    for f in funds:
        for a in portfolios+currencies:
            if str(f)+"_"+str(a) in var:
                f.par.RA_matrix, delta_ra =  RA_matrix_adjustment(portfolios, currencies,funds, a, f,  f.par.cal_change_intensity[a],U[str(f)][str(a)])
                Delta_RA.update({str(f)+"_"+str(a): delta_ra})
            elif str(f)+"_"+str(a) in var_original:
                f.par.RA_matrix, delta_ra = RA_matrix_adjustment(portfolios, currencies,funds, a, f, 0,1)#np.sign(U[str(f)][str(a)]))
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




def RA_matrix_adjustment(portfolios, currencies, funds, asset, fund,  adjustment_intensity, sign):
    """
    Find the next  price of asset a.
    Sums over all demands of funds and exogenous agents
    and calculates the new price in tau via a log impact function
    """
    # Equation 1.18 : Get aggregate demand over all funds and exogenous agents
    D = {}
    for a in portfolios+currencies:
         if str(a)[:2] == "cu":
             if fund.var.currency[a]>0:#a.par.quantity > 0:
                 D.update({a:(fund.var.weights[a]*fund.var.redeemable_shares-fund.var.currency[a]) / fund.var.currency[a]})
                 #D.update({a: (a.par.cash_demand - a.par.quantity)/a.par.quantity})
             else:
                 D.update({a:(fund.var.weights[a]*fund.var.redeemable_shares-fund.var.currency[a]) / fund.var.redeemable_shares})
                 #D.update({a: (a.par.cash_demand - a.par.quantity) / fund.var.redeemable_shares})

         else:
             if fund.var.assets[a] > 0:
                 D.update({a: (fund.var.asset_demand[a]) / fund.var.assets[a]})
             else:
                 D.update({a: (fund.var.asset_demand[a]) / fund.var.redeemable_shares})

    positives = sum([D[a]*(D[a]>0) for a in portfolios+currencies])
    negatives = sum([-D[a]*(D[a]<0) for a in portfolios+currencies])

    if positives ==0 or negatives==0:
        print("problem")

    if (positives<1 or negatives<1) and positives < negatives:
        correction = negatives/float(positives)
        type = "positives"
    elif (positives<1 or negatives<1) and positives > negatives:
        type = "negatives"
        correction = positives / float(negatives)
    else:
        type = "neutral"
        correction = 1




    #demand = demand
    #total_assets = fund.var.redeemable_shares
    DD = D[asset]
    #DD = D*min(100,abs(1/D))

    if type == 'positives' and DD>0:
        DD=DD*correction
    elif type == 'negatives' and DD < 0:
        DD=DD*correction
    risk_aversion_mat = fund.par.RA_matrix.copy()



    risk_aversion_mat.loc[asset][asset]=max(0.1,exp(log(fund.par.RA_matrix.loc[asset][asset]) + sign*adjustment_intensity * (min(1,max(-1,DD)))))
    #Delta = demand / total_assets

    #for c in currencies:
    #    if c.par.country=='domestic':
    #        risk_aversion_mat.loc[c][c] =  risk_aversion_mat.loc[portfolios[0]][portfolios[0]]
    #    if c.par.country == 'foreign':
    #        risk_aversion_mat.loc[c][c] = risk_aversion_mat.loc[portfolios[2]][portfolios[2]]
   ##

    for row in risk_aversion_mat.index:
        for col in risk_aversion_mat.columns:
            risk_aversion_mat.loc[row, col] = np.sqrt(risk_aversion_mat.loc[row, row]) * np.sqrt(
                risk_aversion_mat.loc[col, col])


    return risk_aversion_mat, DD




def int_adjustment(funds, a, adjustment_intensity):
    Delta = (funds[0].exp.returns[a]-funds[0].exp.target_returns[a])/abs(funds[0].exp.target_returns[a])
    log_new_interest = log(a.par.nominal_interest_rate) - adjustment_intensity * Delta
    interest_rate = exp(log_new_interest)


    return interest_rate, Delta



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



def   I_intensity_parameter_adjustment_cal(jump_counter, no_jump_counter, test_sign, Deltas, environment, portfolios,currencies, funds, var):

    portfolios_str = [str(a) for a in portfolios]
    currencies_str = [str(a) for a in currencies]
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
            if a_str[:2]=="cu":
                asset = currencies[currencies_str.index(a_str)]
            else:
                asset = portfolios[portfolios_str.index(a_str)]
            change_intensity = fund.par.cal_change_intensity[asset]
        if np.sign(Deltas[i])==0:
            test[i] = test_sign[i]
        else:
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
            change_intensity =  min(0.9, change_intensity * 1.1)
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