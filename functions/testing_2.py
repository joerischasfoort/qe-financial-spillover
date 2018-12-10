"""Simulation file used to run the model"""


from spillover_model_calRA import *
from spillover_model_calRA2 import *
from spillover_model import *
from calibration_functions import *
from calibration_parts import *
import pandas as pd


seed = 1



saving_params = {}
saving_params.update({"path": 'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects'})

data = open(
        'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\!objects_nonConv_day2635.pkl',
        'rb')
list_of_objects = pickle.load(data)
portfolios_cal = list_of_objects[0]
currencies_cal = list_of_objects[1]
environment_cal = list_of_objects[2]
exogenous_agents_cal = list_of_objects[3]
funds_cal = list_of_objects[4]

environment_cal.par.global_parameters["start_day"] = 2635
environment_cal.par.global_parameters["end_day"] = environment_cal.par.global_parameters["start_day"] + 1000
#environment_cal.par.global_parameters['cov_memory'] = 0
#environment_cal.par.global_parameters['conv_bound'] = 0.01
saving_params.update({"time": 1})
obj_label = "testing"
var = copy.copy(portfolios_cal)
var.append("FX")

portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t_cal = spillover_model(
    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, 1, 1, obj_label,
    saving_params, var)