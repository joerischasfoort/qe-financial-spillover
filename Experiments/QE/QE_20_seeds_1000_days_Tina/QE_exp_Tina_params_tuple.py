import pickle
import time
import os
import sys
import itertools

sys.path.append('/scratch/kzltin001/qe-financial-spillover')

from spillover_model import *

hpc_home = '/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_20_seeds_1000_days_Tina/'

pos = int(os.getenv('SLURM_ARRAY_TASK_ID'))
# 14QE flavours
assets_target = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600]
#20seeds
variable_seeds = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

params_set = list(itertools.product(variable_seeds, assets_target))  #This gives a list with parameter combinations


#when parallel in SLURM/HPC
pos = int(os.getenv('SLURM_ARRAY_TASK_ID'))
tupl= params_set[pos]  #this is a tuple
#slurm array ID to a combination of parameters
print tupl



data = open('/scratch/kzltin001/qe-financial-spillover/Experiments/QE/Objects/CALIBRATED_MASTER_MED.pkl', 'rb')
list_of_objects = pickle.load(data)

portfolios = list_of_objects[0]
currencies = list_of_objects[1]
environment = list_of_objects[2]
exogenous_agents = list_of_objects[3]
funds = list_of_objects[4]
        #seed = list_of_objects[5]
obj_label = list_of_objects[6]

data.close()

saving_params = {}
saving_params.update({"path": '/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_20_seeds_1000_days_Tina/Objects2'})
saving_params.update({"time": 1})

environment.par.global_parameters["start_day"]=2  # Start day 2?
environment.par.global_parameters["end_day"]=1003

environment.par.global_parameters['cov_memory'] = 0
environment.par.global_parameters['conv_bound'] = 0.01
 

exogenous_agents["central_bank_domestic"].var.asset_target[portfolios[0]] = tupl[1]  #take the 1st position in tuple

var = copy.copy(portfolios)
var.append("FX")

seed =  tupl[0]   #take the 0st position in tuple
seed1 = seed

obj_label = "QE_Tina_" + 'seed'+str(seed) + '_' + 'QE'+ str(tupl[1])

portfolios, currencies, environment, exogenous_agents, funds, data_t = spillover_model(portfolios, currencies, environment, exogenous_agents, funds, seed, seed1, obj_label,
            saving_params, var)

  

 