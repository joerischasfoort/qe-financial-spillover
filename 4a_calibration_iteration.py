"""Simulation file used to run the model"""
import time
from spillover_model_calRA import *
from spillover_model import *
from calibration_functions import *
import pandas as pd




seed = 1

saving_params = {}
saving_params.update({"path": 'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects'})
saving_params.update({"time": 2000})




portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, parameters_cal = load_first_run()

portfolios_init, currencies_init, funds_init, environment_init, exogenous_agents_init = init_port_holdings_4f(
    parameters_cal, seed)
#
#funds_cal = approach_balance_sheets(funds_cal,portfolios_cal, currencies_cal, environment_cal, funds_init, portfolios_init, currencies_init, cur_dummy=1)
#
#for fund in funds_cal:
#    for r in range(len(fund.par.RA_matrix.index)):
#        for c in range(len(fund.par.RA_matrix.columns)):
#            fund.par.RA_matrix.iloc[r][c]=5
#
#
#
#
#saving_params.update({"time": 1})
#environment_cal.par.global_parameters["start_day"] = 1
#environment_cal.par.global_parameters["end_day"] = 1001
#environment_cal.par.global_parameters['cov_memory'] =0
#obj_label="new_master"
#portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t_cal = spillover_model(portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, seed, obj_label, saving_params)
#

obj_label = "4a_cal"

convergence = pd.DataFrame([])
convergence_h =  pd.DataFrame([])
for cal_it in range(1,6):


    # first change prices to 1 - slowly
    portfolios_cal = approach_prices(portfolios_cal, approach_speed = 1)
    convergence = convergence.append([sum(abs(a.var.price -  a.var_previous.price) for a in portfolios_cal)])
    writer = pd.ExcelWriter('progress_prev.xlsx')
    convergence.to_excel(writer, 'Sheet1')
    writer.save()

    for f in funds_cal:
        s = recompute_liabilities(f, portfolios_cal, currencies_cal, environment_cal)
        f.var_previous.redeemable_shares = s

    for a in portfolios_cal:
        a.var_previous.price = a.var.price


    var = copy.copy(portfolios_cal)
    var.append("FX")
    environment_cal.par.global_parameters["start_day"] = 1 + 120 * (cal_it - 1)
    environment_cal.par.global_parameters["end_day"] = environment_cal.par.global_parameters["start_day"] + 1
    saving_params.update({"time": environment_cal.par.global_parameters["end_day"] - 1})

    environment_cal.par.global_parameters['cov_memory'] =0
    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t = spillover_model_calRA(portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, seed, obj_label, saving_params,var)



    environment_cal.par.global_parameters["start_day"] = 1 + 120 * (cal_it - 1)
    environment_cal.par.global_parameters["end_day"] = environment_cal.par.global_parameters["start_day"] + 1
    saving_params.update({"time": environment_cal.par.global_parameters["end_day"] - 1})

    environment_cal.par.global_parameters['cov_memory'] =0
    obj_label="4aSim_CalPrices_" + str(cal_it)
    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t_cal = spillover_model(portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, seed, obj_label, saving_params)



#data = open(
#        'C:\Users\jrr\Documents\GitHub\qe-financial-spillover\data\Objects\objects_day_120_seed_1_4aSim_CalPrices_5.pkl',
#        'rb')
#
#
#
#list_of_objects = pickle.load(data)
#
#
#portfolios_cal = list_of_objects[0]
#currencies_cal = list_of_objects[1]
#environment_cal = list_of_objects[2]
#exogenous_agents_cal = list_of_objects[3]
#funds_cal = list_of_objects[4]
#
#
#data.close()
#
#
#
#convergence_h =  pd.DataFrame([])
#convergence_r =  pd.DataFrame([])
#convergence_c =  pd.DataFrame([])
#
#for cal_it2 in range(1,201):
#    #initialize balance sheets
#    obj_label = "4aSim_int_" + str(cal_it2)
#
#    #set prices to 1
#    portfolios_cal = approach_prices(portfolios_cal, approach_speed = 1)
#    for a in portfolios_cal:
#        a.var_previous.price = a.var.price
#
#    for f in funds_cal:
#        s = recompute_liabilities(f, portfolios_cal, currencies_cal, environment_cal)
#        f.var_previous.redeemable_shares = s
#
#    var = copy.copy(portfolios_cal)
#    var.append("FX")
#    environment_cal.par.global_parameters["start_day"] = 1 + 120 * (cal_it2 - 1)
#    environment_cal.par.global_parameters["end_day"] = environment_cal.par.global_parameters["start_day"] + 1
#    environment_cal.par.global_parameters['cov_memory'] = 0
#    saving_params.update({"time": environment_cal.par.global_parameters["end_day"] - 1})
#    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t = spillover_model_calRA(portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, seed, obj_label, saving_params,var)
#
#    funds_cal = approach_balance_sheets(funds_cal, portfolios_cal, currencies_cal, environment_cal, funds_init,
#                                        portfolios_init, currencies_init, cur_dummy=0)
#
#    #update redeemable shares and interest rates
#    var = copy.copy(funds_cal)
#    var.append("FX")
#    environment_cal.par.global_parameters["start_day"] = 1+ 120*(cal_it2-1)
#    environment_cal.par.global_parameters["end_day"] = environment_cal.par.global_parameters["start_day"]+1
#    environment_cal.par.global_parameters['cov_memory'] =0
#    saving_params.update({"time": environment_cal.par.global_parameters["end_day"]-1})
#
#    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t = spillover_model_calRA(portfolios_cal,
#                                                                                                 currencies_cal,
#                                                                                                 environment_cal,
#                                                                                                 exogenous_agents_cal,
#                                                                                                 funds_cal, seed,
#                                                                                                 obj_label,
#                                                                                                 saving_params, var)
#
#
#
#    convergence_h, convergence_r, convergence_c = save_progress(funds_cal, portfolios_cal,convergence_h, convergence_r, convergence_c)
#
#
#
#    environment_cal.par.global_parameters["start_day"] = 1+ 120*(cal_it2-1)
#    environment_cal.par.global_parameters["end_day"] = environment_cal.par.global_parameters["start_day"]+120
#    saving_params.update({"time": environment_cal.par.global_parameters["end_day"]-1})
#    environment_cal.par.global_parameters['cov_memory'] =0
#    obj_label = "4aSim_CalRA_" + str(cal_it2)
#    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t_cal = spillover_model(
#        portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, seed, obj_label, saving_params)
#
#