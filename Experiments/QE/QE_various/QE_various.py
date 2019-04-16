import pickle
import time
import os
import sys
import itertools

sys.path.append('/scratch/kzltin001/qe-financial-spillover')

from spillover_model import *

hpc_home = '/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_10days/'

pos = int(os.getenv('SLURM_ARRAY_TASK_ID'))
 

######Uncomment which QE range you need!!



# # 50!QE flavours
# assets_target = []
# for i in range(0,2550, 100):
# 	assets_target.append(i)

#small range 16QE 
assets_target = [0, 5, 10, 50, 60, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
#20seeds
variable_seeds = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

params_set = list(itertools.product(variable_seeds, assets_target))  #This gives a list with parameter combinations
#Print len to know how many array tasks you need

#when parallel in SLURM/HPC
pos = int(os.getenv('SLURM_ARRAY_TASK_ID'))
tupl= params_set[pos]  #this is a tuple
#slurm array ID to a combination of parameters
print tupl, 'Yay, parameter set is initialised. Program is starting....'



data = open('/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_10days/Med_10days/CALIBRATED_MASTER_MED.pkl', 'rb')
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
saving_params.update({"path": '/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_10days/Med_10days/Objects_10days'})
saving_params.update({"time": 0})

environment.par.global_parameters["start_day"]=2  # Start day 2?
environment.par.global_parameters["end_day"]=12

environment.par.global_parameters['cov_memory'] = 0
environment.par.global_parameters['conv_bound'] = 0.01
 

exogenous_agents["central_bank_domestic"].var.asset_target[portfolios[0]] = tupl[1]  #take the 1st position in tuple

var = copy.copy(portfolios)
var.append("FX")

seed =  tupl[0]   #take the 0st position in tuple
seed1 = seed

obj_label = "Tina_10days_"  + 'QE'+ str(tupl[1])

portfolios, currencies, environment, exogenous_agents, funds, data_t = spillover_model(portfolios, currencies, environment, exogenous_agents, funds, seed, seed1, obj_label,
            saving_params, var)

  
print "Done."
 
