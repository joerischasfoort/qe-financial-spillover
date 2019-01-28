from init_objects_4a import *
from spillover_model import *
from spillover_model_calRA import *
from spillover_model_calRA2 import *
from spillover_model import *
from calibration_functions import *
import pandas as pd

def adjust_interest_rates(funds_cal, portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal,saving_params,iteration, seed, seed1):

    obj_label = "4aSim_intINT_" + str(iteration)


    # set prices to 1
    portfolios_cal = approach_prices(portfolios_cal, approach_speed=1)
    for a in portfolios_cal:
        a.var_previous.price = a.var.price

    #environment_cal.var.fx_rates = environment_init.var.fx_rates.copy()

    for f in funds_cal:
        s = recompute_liabilities(f, portfolios_cal, currencies_cal, environment_cal)
        f.var_previous.redeemable_shares = s

    var = copy.copy(portfolios_cal)
    # var.append("FX")

    environment_cal.par.global_parameters["start_day"] = 1
    environment_cal.par.global_parameters["end_day"] = environment_cal.par.global_parameters["start_day"] + 1
    environment_cal.par.global_parameters['cov_memory'] = 0
    environment_cal.par.global_parameters['conv_bound'] = 0.01
    saving_params.update({"time": environment_cal.par.global_parameters["end_day"] - 1})
    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t = spillover_model_calRA(
        portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, seed, seed1, obj_label,
        saving_params, var)


    return portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal


def adjust_risk_aversion(funds_cal, portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_init, portfolios_init, currencies_init, saving_params, iteration, seed, seed1, int_adjustment):

    funds_cal, portfolios_cal = approach_balance_sheets(funds_cal, portfolios_cal, currencies_cal, environment_cal,
                                                        funds_init,
                                                        portfolios_init, currencies_init, cur_dummy=1)
    # update redeemable shares and interest rates
    var = [str(f) + "_" + str(a) for f in funds_cal for a in portfolios_cal + currencies_cal]
    if int_adjustment == True:
        for a in portfolios_cal:
            var.append(a)
    # var.append("FX")
    environment_cal.par.global_parameters["start_day"] = 1
    environment_cal.par.global_parameters["end_day"] = environment_cal.par.global_parameters["start_day"] + 1
    environment_cal.par.global_parameters['cov_memory'] = 0
    environment_cal.par.global_parameters['conv_bound'] = 0.01
    saving_params.update({"time": environment_cal.par.global_parameters["end_day"] - 1})
    obj_label = "4aSim_intRA_" + str(iteration)
    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, success = spillover_model_calRA2(
        portfolios_cal,
        currencies_cal,
        environment_cal,
        exogenous_agents_cal,
        funds_cal, seed, seed1,
        obj_label,
        saving_params, var)

    return portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, success



def simulate(portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, saving_params, iteration, seed, seed1,days):
    environment_cal.par.global_parameters["start_day"] = 2
    environment_cal.par.global_parameters["end_day"] = environment_cal.par.global_parameters["start_day"] + days
    environment_cal.par.global_parameters['cov_memory'] = 0
    environment_cal.par.global_parameters['conv_bound'] = 0.01
    saving_params.update({"time": environment_cal.par.global_parameters["end_day"] - 1})
    obj_label = "4aSim_Cal_" + str(iteration)
    var = copy.copy(portfolios_cal)
    var.append("FX")

    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t_cal = spillover_model(
        portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, seed, seed1, obj_label,
        saving_params,var)

    return portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal