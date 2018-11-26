"""Simulation file used to run the model"""


from spillover_model_calRA import *
from spillover_model_calRA2 import *
from spillover_model import *
from calibration_functions import *
from calibration_parts import *
import pandas as pd


seed = 1



saving_params = {}
saving_params.update({"path": 'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects_final'})

#portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal= initial_simulation(seed)

#
portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal = load_first_run(seed)
#
for a in portfolios_cal:
    a.par.cal_change_intensity = 0.01

portfolios_init, currencies_init, funds_init, environment_init, exogenous_agents_init = init_port_holdings_4f(seed)
#
# including the full risk aversion matrix
#for f in funds_cal:
#    f.par.RA_matrix = f.var.covariance_matrix.copy()
#    for row in range(len(f.par.RA_matrix.index)):  # 2 initalise model objects
#        for col in range(len(f.par.RA_matrix.index)):
#            f.par.RA_matrix.iloc[row, col] = 2
#
environment_cal.par.global_parameters['domestic_inflation_mean'] = 0.01/float(250)
environment_cal.par.global_parameters['foreign_inflation_mean'] = 0.021/float(250)
environment_cal.par.global_parameters['domestic_inflation_std'] = 0.01/float(250)
environment_cal.par.global_parameters['foreign_inflation_std'] = 0.007/float(250)
for f in funds_cal:
    f.exp.inflation = {"domestic": environment_cal.par.global_parameters['domestic_inflation_mean'],
                       "foreign": environment_cal.par.global_parameters['foreign_inflation_mean']}

currencies_cal[0].par.nominal_interest_rate = -0.002/float(250)
currencies_cal[1].par.nominal_interest_rate = 0.0085/float(250)

# target returns
environment_cal.par.global_parameters[portfolios_cal[0]] =   (1+0.009/float(250))/(1+environment_cal.par.global_parameters['domestic_inflation_mean'])-1
environment_cal.par.global_parameters[portfolios_cal[1]] =  (1+0.063/float(250))/(1+environment_cal.par.global_parameters['domestic_inflation_mean'])-1
environment_cal.par.global_parameters[portfolios_cal[2]] =   (1+0.019/float(250))/(1+environment_cal.par.global_parameters['foreign_inflation_mean'])-1
environment_cal.par.global_parameters[portfolios_cal[3]] =  (1+0.071/float(250))/(1+environment_cal.par.global_parameters['foreign_inflation_mean'])-1
# adjust to former expectations
for f in funds_cal:
    f.exp.target_returns = {a: environment_cal.par.global_parameters[a]*environment_cal.var.fx_rates.loc[f.par.country, a.par.country] for a in portfolios_cal}




#portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal = simulate(portfolios_cal,
#                                                                                                currencies_cal,
#                                                                                                environment_cal,
#                                                                                                exogenous_agents_cal,
#                                                                                                funds_cal, saving_params,
#                                                                                                0,
#                                                                                                seed, seed,1001)
#
#
#
#





data = open(
        'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects_final\objects_day_1002_seed_1_4aSim_Cal_0.pkl',
        'rb')
list_of_objects = pickle.load(data)
portfolios_cal = list_of_objects[0]
currencies_cal = list_of_objects[1]
environment_cal = list_of_objects[2]
exogenous_agents_cal = list_of_objects[3]
funds_cal = list_of_objects[4]
#

for f in funds_cal:
    f.par.cal_change_intensity = {a: 0.1 for a in portfolios_cal + currencies_cal}
#



convergence_h =  pd.DataFrame([])
convergence_r =  pd.DataFrame([])
convergence_c =  pd.DataFrame([])



currencies_cal[0].par.quantity = sum([f.var.currency[currencies_init[0]] for f in funds_init])
currencies_cal[1].par.quantity = sum([f.var.currency[currencies_init[0]] for f in funds_init])
#currencies_cal[0].par.quantity = 200
#currencies_cal[1].par.quantity = 2500


for c in currencies_cal:
    c.par.RA = 1
    c.par.cal_change_intensity = 0.1


for cal_it2 in range(1,501):
    seed1 = cal_it2

    environment_cal.var.fx_rates = environment_init.var.fx_rates.copy()

    for a in portfolios_cal:
        a.par.cal_change_intensity = max(0.01,  a.par.cal_change_intensity)
    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal = adjust_interest_rates(funds_cal, portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal,
                          saving_params, cal_it2, seed, seed1)

    for f in funds_cal:
        f.par.cal_change_intensity = {a: max(f.par.cal_change_intensity[a],0.01) for a in portfolios_cal + currencies_cal}
    int_adjustment = False
    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, success = adjust_risk_aversion(funds_cal, portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal,funds_init, portfolios_init, currencies_init, saving_params, cal_it2, seed, seed1,int_adjustment)



    convergence_h, convergence_r, convergence_c = save_progress(funds_cal, portfolios_cal,convergence_h, convergence_r, convergence_c)



    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal = simulate(portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, saving_params, cal_it2,
             seed, seed1,101)