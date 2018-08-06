import  pickle
import time
import os
import sys


sys.path.append('/home/jriedler/qe-financial-spillover')

from spillover_model import *




hex_home = '/home/jriedler/qe-financial-spillover/Experiments/QE_wHB/'

variable = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]


#when parallel
at=[0]
pos = int(os.getenv('PBS_ARRAYID'))
at[0]=variable[pos]



for i in at:

    data = open(hex_home + 'Objects_QE_wHB/objects_day_4999_seed_1_RA_' + str(variable[pos]) + '.pkl', 'rb')

    list_of_objects = pickle.load(data)

    portfolios = list_of_objects[0]
    currencies = list_of_objects[1]
    environment = list_of_objects[2]
    exogeneous_agents = list_of_objects[3]
    funds = list_of_objects[4]
    seed = list_of_objects[5]
    obj_label = list_of_objects[6]

    data.close()

    environment.par.global_parameters["start_day"]=5000
    environment.par.global_parameters["end_day"]=7001



    exogeneous_agents["central_bank_domestic"].var.asset_target[portfolios[0]] = 500

    obj_label="QE_RA_"+str(i)
    
    saving_params = {}
    saving_params.update({"path": '/home/jriedler/qe-financial-spillover/Experiments/QE/Objects_QE_wHB/'})
    saving_params.update({"time": 0})

    print(i)
    portfolios, currencies, environment, exogeneous_agents, funds, data_t = spillover_model(portfolios, currencies, environment, exogeneous_agents, funds,  seed, obj_label, saving_params)

