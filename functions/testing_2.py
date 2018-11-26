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
        'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects\!nonConv_time_seed_1_day_1_tau_1000_4aSim_intRA_0_start.pkl',
        'rb')
list_of_objects = pickle.load(data)
portfolios_cal = list_of_objects[0]
currencies_cal = list_of_objects[1]
environment_cal = list_of_objects[2]
exogenous_agents_cal = list_of_objects[3]
funds_cal = list_of_objects[4]


#
for a in portfolios_cal:
    a.par.cal_change_intensity = 0.01

portfolios_init, currencies_init, funds_init, environment_init, exogenous_agents_init = init_port_holdings_4f(seed)
#




success = False
while success == False:
    int_adjustment = False
    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, success = adjust_risk_aversion(funds_cal,
                                                                                                            portfolios_cal,
                                                                                                            currencies_cal,
                                                                                                            environment_cal,
                                                                                                            exogenous_agents_cal,
                                                                                                            funds_init,
                                                                                                            portfolios_init,
                                                                                                            currencies_init,
                                                                                                            saving_params,
                                                                                                            0, seed,
                                                                                                            seed, int_adjustment )

#

