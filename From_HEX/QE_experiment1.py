import  pickle
from spillover_model_QE1 import *
import time
import os


hex_home = '/home/jriedler/qe-financial-spillover/Experiments/QE/'

#reset -f
assets_target = [0, 100,200,300,400,500,600,700,800,900,1000]


#when parallel
at=[0]
pos = int(os.getenv('PBS_ARRAYID'))
at[0]=assets_target[pos]

for i in at:

    data = open(hex_home + 'Objects_QE1/objects_day_4999_seed_1_mat_0.9992.pkl', 'rb')

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
    environment.par.global_parameters["end_day"]=8000



    environment.par.global_parameters["fx_reversion_speed"]=0


    exogeneous_agents["central_bank_domestic"].var.asset_target[portfolios[0]] = i

    obj_label="QE_asset_target_"+str(i)
    start = time.time()
    portfolios, currencies, environment, exogeneous_agents, funds, data_t = spillover_model_QE1(portfolios, currencies, environment, exogeneous_agents, funds,  seed, obj_label)
    end = time.time()
    print(i, end - start)
