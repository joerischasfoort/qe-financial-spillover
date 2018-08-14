import  pickle
import time
import os
import sys


sys.path.append('/home/kzltin001/qe-financial-spillover')

from spillover_model import *




hex_home = '/home/kzltin001/qe-financial-spillover/Experiments/Sym_4assets/'

variable = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]


#when parallel
at=[0]
pos = int(os.getenv('PBS_ARRAYID'))
at[0]=variable[pos]



for i in at:

    data = open(hex_home + 'Sym_4assets/objects_day_4999_seed_1_RA_' + str(variable[pos]) + '.pkl', 'rb')

    list_of_objects = pickle.load(data)

    portfolios = list_of_objects[0]
    currencies = list_of_objects[1]
    environment = list_of_objects[2]
    exogeneous_agents = list_of_objects[3]
    funds = list_of_objects[4]
    seed = list_of_objects[5]
    obj_label = list_of_objects[6]

    data.close()

    environment.par.global_parameters["start_day"]=3000
    environment.par.global_parameters["end_day"]=5000


    
    exogeneous_agents["central_bank_domestic"].var.asset_target[portfolios[0]] = 500

    obj_label="Sym_4assets"+str(i)
    
    saving_params = {}
    saving_params.update({"path": '/home/kzltin001/qe-financial-spillover/Experiments/Sym_4assets/Objects_Sym_4assets/'})
    saving_params.update({"time": 0})

    print(i)
    portfolios, currencies, environment, exogeneous_agents, funds, data_t = spillover_model(portfolios, currencies, environment, exogeneous_agents, funds,  seed, obj_label, saving_params)

