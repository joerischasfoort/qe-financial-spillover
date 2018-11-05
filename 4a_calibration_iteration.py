"""Simulation file used to run the model"""


from spillover_model_calRA import *
from spillover_model import *
from calibration_functions import *
import pandas as pd






saving_params = {}
saving_params.update({"path": 'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects'})

portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal= initial_simulation(seed)


#portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal = load_first_run(seed)

for a in portfolios_cal:
    a.par.cal_change_intensity = 0.01

portfolios_init, currencies_init, funds_init, environment_init, exogenous_agents_init = init_port_holdings_4f(seed)
#



for f in funds_cal:
    f.par.cal_change_intensity = {a: 0.01 for a in portfolios_cal}


convergence_h =  pd.DataFrame([])
convergence_r =  pd.DataFrame([])
convergence_c =  pd.DataFrame([])




for cal_it2 in range(301,501):
    #initialize balance sheets
    obj_label = "4aSim_int_" + str(cal_it2)

    #set prices to 1
    portfolios_cal = approach_prices(portfolios_cal, approach_speed = 1)
    for a in portfolios_cal:
        a.var_previous.price = a.var.price

    for f in funds_cal:
        s = recompute_liabilities(f, portfolios_cal, currencies_cal, environment_cal)
        f.var_previous.redeemable_shares = s

    var = copy.copy(portfolios_cal)
    var.append("FX")





    environment_cal.par.global_parameters["start_day"] = 5001
    environment_cal.par.global_parameters["end_day"] = environment_cal.par.global_parameters["start_day"] + 1
    environment_cal.par.global_parameters['cov_memory'] = 0
    environment_cal.par.global_parameters['conv_bound']=0.001
    saving_params.update({"time": environment_cal.par.global_parameters["end_day"] - 1})
    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t = spillover_model_calRA(portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, seed, obj_label, saving_params,var)

    funds_cal = approach_balance_sheets(funds_cal, portfolios_cal, currencies_cal, environment_cal, funds_init,
                                        portfolios_init, currencies_init, cur_dummy=0)

    #update redeemable shares and interest rates
    var = [str(f)+"_"+str(a) for f in funds_cal for a in  portfolios_cal]
    var.append("FX")
    environment_cal.par.global_parameters["start_day"] = 5001
    environment_cal.par.global_parameters["end_day"] = environment_cal.par.global_parameters["start_day"] + 1
    environment_cal.par.global_parameters['cov_memory'] = 0
    environment_cal.par.global_parameters['conv_bound']=0.01
    saving_params.update({"time": environment_cal.par.global_parameters["end_day"]-1})

    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t = spillover_model_calRA(portfolios_cal,
                                                                                                 currencies_cal,
                                                                                                 environment_cal,
                                                                                                 exogenous_agents_cal,
                                                                                                 funds_cal, seed,
                                                                                                 obj_label,
                                                                                                 saving_params, var)



    convergence_h, convergence_r, convergence_c = save_progress(funds_cal, portfolios_cal,convergence_h, convergence_r, convergence_c)



    environment_cal.par.global_parameters["start_day"] = 5001
    environment_cal.par.global_parameters["end_day"] = environment_cal.par.global_parameters["start_day"] + 101
    environment_cal.par.global_parameters['cov_memory'] = 0
    environment_cal.par.global_parameters['conv_bound']=0.01
    saving_params.update({"time": environment_cal.par.global_parameters["end_day"]-1})
    obj_label = "4aSim_CalRA_" + str(cal_it2)
    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t_cal = spillover_model(
        portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, seed, obj_label, saving_params)
