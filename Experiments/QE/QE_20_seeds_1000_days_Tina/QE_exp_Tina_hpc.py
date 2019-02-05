import pickle
import time
import os
import sys


sys.path.append('/scratch/kzltin001/qe-financial-spillover')

from spillover_model import *




hpc_home = '/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_20_seeds_1000_days_Tina/'



pos = int(os.getenv('SLURM_ARRAY_TASK_ID'))

import itertools
#
assets_target = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600]
#20seeds
variable_seeds = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

params_set = list(itertools.product(variable_seeds, assets_target))




assets_target = [0, 50, 100 , 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
variable_seeds = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20, 21, 22, 23, 24, 25]
#when parallel in SLURM/HPC


pos = int(os.getenv('SLURM_ARRAY_TASK_ID'))

params_set = list(itertools.product(variable_seeds,assets_target))



params_set = [pos]
#slurm array ID to a combination of parameters
for i in params_set:
    params_set = {}

    for i in assets_target:
        if 'QE' not in params_set:
            params_set['QE'] = []

        if 'seed' not in params_set:
            params_set['seed'] = []

        params_set['QE'].append(i)
        params_set['seed'].append(variable_seeds[pos])


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
        saving_params.update({"path": '/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_20_seeds_1000_days_Tina/Objects'})
        saving_params.update({"time": 1})

        environment.par.global_parameters["start_day"]=2  # Start day 2?
        environment.par.global_parameters["end_day"]=1003

        environment.par.global_parameters['cov_memory'] = 0
        environment.par.global_parameters['conv_bound'] = 0.01

        exogenous_agents["central_bank_domestic"].var.asset_target[portfolios[0]] = params_set['QE'][-1]  #take the last

        var = copy.copy(portfolios)
        var.append("FX")

        seed =  params_set['seed'][-1]
        seed1 = seed

        obj_label = "QE_Tina_" + 'seed'+str(params_set['seed'][-1]) + '_' + 'QE'+ str(params_set['QE'][-1])

        portfolios, currencies, environment, exogenous_agents, funds, data_t = spillover_model(
            portfolios, currencies, environment, exogenous_agents, funds, seed, seed1, obj_label,
            saving_params, var)

    return params_set


params = run(pos)
print params