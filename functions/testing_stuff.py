"""Simulation file used to run the model"""
import time
from spillover_model_calRA import *
from spillover_model import *
from calibration_functions import *
import pandas as pd
from stochasticprocess import *
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import math

data = open(
            'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects\objects_day_557_seed_1_master.pkl',
            'rb')

seed=1
list_of_objects = pickle.load(data)


portfolios_cal = list_of_objects[0]
currencies_cal = list_of_objects[1]
environment_cal = list_of_objects[2]
exogenous_agents_cal = list_of_objects[3]
funds_cal = list_of_objects[4]


data.close()

saving_params = {}
saving_params.update({"path": 'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects'})
saving_params.update({"time": 0})

obj_label = "master"

environment_cal.par.global_parameters["start_day"] = 558
environment_cal.par.global_parameters["end_day"] = 5001

portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t_cal = spillover_model(
    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, seed, obj_label, saving_params)



