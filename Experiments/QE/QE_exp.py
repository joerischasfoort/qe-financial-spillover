import  pickle
from spillover_model_QE import *
import time
import os


hex_home = '/home/jriedler/qe-financial-spillover/Experiments/QE/'


#reset -f
assets_target = [0, 20,40,60,80,100,120,140,160,180,200,250,300,350,400,450,500]

for i in assets_target:

    data = open('C:\Users\jrr\Documents\GitHub\qe-financial-spillover\Experiments\QE\Objects_QE\objects_day_5000_seed_1_lcrw_0.9999.pkl', 'rb')

    list_of_objects = pickle.load(data)

    portfolios = list_of_objects[0]
    currencies = list_of_objects[1]
    environment = list_of_objects[2]
    exogeneous_agents = list_of_objects[3]
    funds = list_of_objects[4]
    seed = list_of_objects[5]
    obj_label = list_of_objects[6]

    data.close()

    environment.par.global_parameters["start_day"]=5001
    environment.par.global_parameters["end_day"]=5101



    exogeneous_agents["central_bank_domestic"].var.asset_target[portfolios[0]] = i

    obj_label="QE_asset_target_"+str(i)
    start = time.time()
    portfolios, currencies, environment, exogeneous_agents, funds, data_t = spillover_model_QE(portfolios, currencies, environment, exogeneous_agents, funds,  seed, obj_label)
    end = time.time()
    print(i, end - start)
