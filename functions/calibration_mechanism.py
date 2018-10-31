from __future__ import division
from math import log
from math import exp
import numpy as np

def update_RA_and_fx(portfolios, environment,currencies, funds,exogeneous_agents, var):
    Delta_RA = {}
    Delta_Demand = {}
    Delta_Capital = {}
    Delta_eDR = { }
    Delta_aDR = {}
    change_intensity = 0.1
    for a in np.random.permutation(portfolios):
        if a in var:
            a.par.nominal_interest_rate, delta_demand = interest_rate_adjustment(portfolios, exogeneous_agents, funds, a, 0.01)  # TODO: is the Delta_str really necessary?
            Delta_Demand.update({a: delta_demand})
        else:
            a.par.nominal_interest_rate, delta_demand = interest_rate_adjustment(portfolios, exogeneous_agents, funds, a, 0)  # TODO: is the Delta_str really necessary?
            Delta_Demand.update({a: delta_demand})

#    for f in funds:
#        if f in var:
#            f.par.risk_aversion, delta_ra = RA_adjustment(portfolios, f, f.par.change_intensity)
#            Delta_RA.update({f: delta_ra})
#        else:
#            f.par.risk_aversion, delta_ra = RA_adjustment(portfolios, f,{"domestic_asset":0,"foreign_asset":0})
#            Delta_RA.update({f: delta_ra})

    for f in np.random.permutation(funds):
        if f in var:
            f.par.RA_matrix, delta_ra =  RA_matrix_adjustment(portfolios, currencies, f, funds, 0.1)
            Delta_RA.update({f: delta_ra})
        #else:
         #   f.par.RA_matrix, delta_ra = RA_matrix_adjustment(portfolios, currencies, f, 0.0)
          #  Delta_RA.update({f: delta_ra})

        environment.var.fx_rates, Delta_Capital = fx_adjustment(portfolios, currencies, environment, funds,
                                                                0)

    if "FX" in var:
        environment.var.fx_rates, Delta_Capital = fx_adjustment(portfolios, currencies, environment, funds,
                                                                environment.par.global_parameters[
                                                                    "fx_change_intensity"])


    if "equity_dr" in var:
        default_rate_mean, Delta_eDR=default_rate_adjustment(portfolios, exogeneous_agents, funds, change_intensity)
        for a in portfolios:
            if a.par.maturity == 1:
                a.par.default_rate_mean=default_rate_mean/float(a.par.mean_default_events*250)


    if "all_dr" in var:
        tot_avg_events = 0
        for a in portfolios:
            if a.par.maturity<1:
                tot_avg_events += a.par.mean_default_events*250

        a_default_rates, Delta_aDR = all_default_rates_adjustment(portfolios, funds, 0.1)
        for dr in a_default_rates:
            for a in portfolios:
                if a.par.maturity == 1 and dr.split("_")[0]=="e" and dr.split("_")[1]==a.par.country:
                    a.par.default_rate_mean=a_default_rates[dr]/float(a.par.mean_default_events*250)
              #  if a.par.maturity < 1 and dr.split("_")[0]=="b" and dr.split("_")[1]==a.par.country:
              #      a.par.default_rate_mean = a_default_rates[dr] / float(a.par.mean_default_events * 250)
              #  if a.par.maturity < 1 and dr.split("_")[0] == "b" and dr.split("_")[1] != a.par.country:
              #      a.par.default_rate_mean = ((0.02*tot_avg_events)-a_default_rates[dr]*(tot_avg_events-a.par.mean_default_events * 250))/ (float(a.par.mean_default_events * 250)**2)




    Deltas = {}
    Deltas.update(Delta_RA)
    Deltas.update(Delta_Demand)
    Deltas.update({"FX": Delta_Capital})
    Deltas.update(Delta_eDR)

    Deltas.update(Delta_aDR)

    return funds, environment, portfolios, Deltas

def RA_adjustment(portfolios, fund, adjustment_intensity):
    """
    Find the next  price of asset a.
    Sums over all demands of funds and exogenous agents
    and calculates the new price in tau via a log impact function
    """
    # Equation 1.18 : Get aggregate demand over all funds and exogenous agents
    domestic_demand = 0
    foreign_demand = 0
    domestic_assets = 0
    foreign_assets = 0


    for asset in portfolios:
        if asset.par.country == "domestic":
            domestic_demand += fund.var.asset_demand[asset]
            domestic_assets += fund.var.assets[asset]
        else:
            foreign_demand += fund.var.asset_demand[asset]
            foreign_assets += fund.var.assets[asset]



    total_quantity = sum(a.par.quantity for a in portfolios)

    # Equation 1.17 : price adjustment
    log_new_ra_domestic = log(fund.par.risk_aversion["domestic_asset"]) + adjustment_intensity["domestic_asset"] * domestic_demand / domestic_assets
    log_new_ra_foreign = log(fund.par.risk_aversion["foreign_asset"]) + adjustment_intensity[
        "foreign_asset"] * foreign_demand / foreign_assets

    risk_aversion={}
    risk_aversion.update({"domestic_asset": exp(log_new_ra_domestic)})
    risk_aversion.update({"foreign_asset": exp(log_new_ra_foreign)})


    Delta = (foreign_demand+domestic_demand) / total_quantity

    return risk_aversion, Delta




def RA_matrix_adjustment(portfolios, currencies, fund, funds, adjustment_intensity):
    """
    Find the next  price of asset a.
    Sums over all demands of funds and exogenous agents
    and calculates the new price in tau via a log impact function
    """
    # Equation 1.18 : Get aggregate demand over all funds and exogenous agents
    demand = {a: 0 for a in portfolios}

    total_assets = {a: 0 for a in portfolios}


    for asset in portfolios:
        demand.update({asset: fund.var.asset_demand[asset]})
        total_assets.update({asset: fund.var.assets[asset]})
    for cur in currencies:
        demand.update({cur: fund.var.currency_demand[cur]})
        total_assets.update({cur: fund.var.currency[cur]})

    risk_aversion_mat = fund.par.RA_matrix.copy()

    Delta_h = []
    for a in np.random.permutation(portfolios):
        risk_aversion_mat.loc[a][a]=exp(log(fund.par.RA_matrix.loc[a][a]) + adjustment_intensity * demand[a] / total_assets[a])
        Delta_h.append(abs(demand[a] / total_assets[a]))
    for c in currencies:
        risk_aversion_mat.loc[c][c] = 5
    #    if c.par.country=='domestic':
    #        risk_aversion_mat.loc[c][c] =  risk_aversion_mat.loc[portfolios[0]][portfolios[0]]
    #    if c.par.country == 'foreign':
    #        risk_aversion_mat.loc[c][c] = risk_aversion_mat.loc[portfolios[2]][portfolios[2]]
    #    if fund in [funds[0], funds[2]]: # these are the investment funds
    #        risk_aversion_mat.loc[c][c] = 10e5 #it is not part of their business model to hold currency beyound transactional purposes
    #    else:
    #        if c.par.country==fund.par.country:
    #            risk_aversion_mat.loc[c][c] = exp(
    #                log(fund.par.RA_matrix.loc[c][c]) + adjustment_intensity * demand[c] / total_assets[c])
    #            Delta_h.append(abs(demand[c] / total_assets[c]))
    #           # risk_aversion_mat.loc[c][c] = 0
    #        if c.par.country!=fund.par.country:
    #            risk_aversion_mat.loc[c][c] = 10e5 # equal to the risk aversion for bonds

    Delta = max(Delta_h)

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





def default_rate_adjustment(portfolios, exogeneous_agents, funds, adjustment_intensity):

    total_demand_equity = 0
    total_demand_exogenous_agents_equity = 0
    quantity_home = {f: 0 for f in funds}
    equity_demand_home = {f: 0 for f in funds}
    bond_demand_home = {f: 0 for f in funds}
    excess_home_equity_demand = {f: 0 for f in funds}

    default_rate_old = portfolios[1].par.default_rate_mean*float(portfolios[1].par.mean_default_events*250)


    for f in funds:
        for a in portfolios:
            if a.par.country==f.par.country:
                quantity_home[f] += f.var.assets[a]
            if a.par.maturity ==1 and a.par.country==f.par.country:
                equity_demand_home[f] += f.var.asset_demand[a]
            if a.par.maturity <1 and a.par.country==f.par.country:
                bond_demand_home[f] += f.var.asset_demand[a]

        excess_home_equity_demand[f] =  (equity_demand_home[f])/float(quantity_home[f])

    total_ex_equity = sum(excess_home_equity_demand[f] for f in funds)


    # Equation 1.17 : price adjustment
    log_new_dr = log(default_rate_old) + adjustment_intensity * (total_ex_equity)

    default_rate = exp(log_new_dr)

    Delta_DR = {"equity_dr": total_ex_equity}

    return default_rate,  Delta_DR




def all_default_rates_adjustment(portfolios, funds, adjustment_intensity):


    equity_demand_domestic = {f: 0 for f in funds}
    equity_demand_foreign = {f: 0 for f in funds}
    bond_demand_domestic = {f: 0 for f in funds}
    bond_demand_foreign = {f: 0 for f in funds}

    old_default_rates = {}
    quantities = {}
    demands = {}

    for a in portfolios:
        if a.par.maturity == 1 and a.par.country == "domestic":
            quantities.update({"e_domestic": a.par.quantity})
            old_default_rates.update({"e_domestic": a.par.default_rate_mean*float(a.par.mean_default_events*250)})
        if a.par.maturity == 1 and a.par.country == "foreign":
            quantities.update({"e_foreign": a.par.quantity})
            old_default_rates.update({"e_foreign": a.par.default_rate_mean * float(a.par.mean_default_events * 250)})
        if a.par.maturity < 1 and a.par.country == "domestic":
            quantities.update({"b_domestic": a.par.quantity})
            old_default_rates.update({"b_domestic": a.par.default_rate_mean * float(a.par.mean_default_events * 250)})
        if a.par.maturity < 1 and a.par.country == "foreign":
            quantities.update({"b_foreign": a.par.quantity})
            old_default_rates.update({"b_foreign": a.par.default_rate_mean * float(a.par.mean_default_events * 250)})



    for f in funds:
        for a in portfolios:
            if a.par.maturity ==1 and a.par.country=="domestic":
                equity_demand_domestic[f] += f.var.asset_demand[a]
            if a.par.maturity <1 and a.par.country=="domestic":
                bond_demand_domestic[f] += f.var.asset_demand[a]
            if a.par.maturity ==1 and a.par.country=="foreign":
                equity_demand_foreign[f] += f.var.asset_demand[a]
            if a.par.maturity <1 and a.par.country=="foreign":
                bond_demand_foreign[f] += f.var.asset_demand[a]

    demands.update({"e_domestic": sum(equity_demand_domestic[f] for f in funds)/quantities["e_domestic"]})
    demands.update({"e_foreign": sum(equity_demand_foreign[f] for f in funds)/quantities["b_foreign"]})
    demands.update({"b_domestic": sum(bond_demand_domestic[f] for f in funds)/quantities["e_domestic"]})
    demands.update({"b_foreign": sum(bond_demand_foreign[f] for f in funds)/quantities["b_foreign"]})

    Delta = {}
    new_default_rates = {}
    for d in demands:
        if d.split("_")[0] == "e":
            new_default_rates.update({d: exp(log(old_default_rates[d]) + adjustment_intensity * demands[d])})
            Delta.update({d:demands[d]})
        if d == "b_domestic" and abs(demands[d])>=abs(demands["b_foreign"]):
            new_default_rates.update({d: exp(log(old_default_rates[d]) + adjustment_intensity * demands[d])})
            Delta.update({d:demands[d]})
        if d == "b_foreign" and abs(demands[d]) > abs(demands["b_domestic"]):
            new_default_rates.update({d: exp(log(old_default_rates[d]) + adjustment_intensity * demands[d])})
            Delta.update({d:demands[d]})


    return new_default_rates,  Delta





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



def   I_intensity_parameter_adjustment(jump_counter, no_jump_counter, test_sign, Deltas, convergence, environment, var):

    jc = 5 # jumps until intensity is adjusted
    nojc = 10 # consecutive non-jumps until intensity is adjusted
    test = {}
    jump = {x:0 for x in jump_counter}
    no_jump = {x:0 for x in jump_counter}

    for i in jump_counter:
        test[i] = test_sign[i] / np.sign(Deltas[i])
        test_sign[i] = np.sign(Deltas[i])

        if test[i] == -1:
            jump[i] = 1
        if test[i] == 1:
            no_jump[i] = 1

        if jump[i] == 1 and i in var:
            jump_counter[i] += 1
            no_jump_counter[i] = 0

        if no_jump[i] == 1 and i in var:
            no_jump_counter[i] += 1

        if jump_counter[i] > jc and i!="FX" and i in var and convergence[i] == False:
            i.par.change_intensity = i.par.change_intensity  / 3
            jump_counter[i] = 0
            no_jump_counter[i]=0


        if jump_counter[i] > jc and i == "FX" and i in var and convergence[i] == False:
            environment.par.global_parameters['fx_change_intensity'] = environment.par.global_parameters['fx_change_intensity'] / 3
            jump_counter[i] = 0
            no_jump_counter[i]=0


        if no_jump_counter[i] > nojc and i!="FX" and i in var and convergence[i] == False:
            i.par.change_intensity =  min(0.1, i.par.change_intensity * 1.1)
            no_jump_counter[i] = 0
            jump_counter[i] = 0


        if no_jump_counter[i] > nojc and i=="FX" and i in var and convergence[i] == False:
            environment.par.global_parameters['fx_change_intensity'] = min(0.1, environment.par.global_parameters['fx_change_intensity'] * 1.1)
            no_jump_counter[i] = 0
            jump_counter[i] = 0


    return  jump_counter, no_jump_counter, test_sign, environment



def check_convergence_cal(Deltas, conv_bound, funds, tau):
    convergence_bound = {}
    convergence_bound.update({i: conv_bound for i in Deltas})
    convergence_bound.update({"FX": conv_bound})
    convergence_bound.update({"equity_dr": conv_bound/10})


    convergence_condition = {i: abs(Deltas[i]) < convergence_bound[i] for i in Deltas}
    #ra_convergence = sum([convergence_condition[f] for f in funds])
    convergence = sum(convergence_condition[i] for i in convergence_condition) == len(Deltas) and tau > 20

    if tau > 1000: convergence = True  # exit iteration after many iterations

    return convergence, convergence_condition