import pickle
import time
import os
import sys
import itertools

sys.path.append('/scratch/kzltin001/qe-financial-spillover')

from spillover_model import *

hpc_home = '/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_2500_2750/'

pos = int(os.getenv('SLURM_ARRAY_TASK_ID'))
# 14QE flavours

assets_target = [0, 100, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600]

#30seeds
variable_seeds = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

params_set = list(itertools.product(variable_seeds, assets_target))  #This gives a list with parameter combinations
print(len(params_set), "combinations")

#when parallel in SLURM/HPC
pos = int(os.getenv('SLURM_ARRAY_TASK_ID'))
tupl= params_set[pos]  #this is a tuple
#slurm array ID to a combination of parameters
print tupl, 'parameter set is initialised! :)'



data = open('/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_2500_2750/CALIBRATED_MASTER_MAX.pkl', 'rb')
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
saving_params.update({"path": '/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_2500_2750/Max_Cal_Objects'})
saving_params.update({"time": 2499})

environment.par.global_parameters["start_day"]=2  # Start day 2?
environment.par.global_parameters["end_day"]=2751

environment.par.global_parameters['cov_memory'] = 0
environment.par.global_parameters['conv_bound'] = 0.01
 

exogenous_agents["central_bank_domestic"].var.asset_target[portfolios[0]] = tupl[1]  #take the 1st position in tuple

var = copy.copy(portfolios)
var.append("FX")

seed =  tupl[0]   #take the 0st position in tuple
seed1 = seed

obj_label = "2500_2750_max_"  + 'QE'+ str(tupl[1])

portfolios, currencies, environment, exogenous_agents, funds, data_t = spillover_model(portfolios, currencies, environment, exogenous_agents, funds, seed, seed1, obj_label,
            saving_params, var)

  

 
