import  pickle
import time
import os
import sys


sys.path.append('/home/jriedler/qe-financial-spillover')

from spillover_model import *




hex_home = '/home/jriedler/qe-financial-spillover/Experiments/QE/'

#variable = [0, 100,200,300,400,500,600]
variable = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20, 21, 22, 23]


#when parallel
at=[0]
pos = int(os.getenv('PBS_ARRAYID'))
at[0]=variable[pos]

target = 400

for i in at:


    data = open('/home/jriedler/qe-financial-spillover/Experiments/QE/Objects_QE_med/CALIBRATED_MASTER_MED.pkl', 'rb')
    #data = open('C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects\CALIBRATED_MASTER_MED.pkl', 'rb')


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
    saving_params.update({"path": '/home/kltin001/qe-financial-spillover/Experiments/QE/Objects_QE_med'})
    #saving_params.update({"path": 'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects'})
    saving_params.update({"time": 1})


    environment.par.global_parameters["start_day"]=2
    environment.par.global_parameters["end_day"]=1003



    exogenous_agents["central_bank_domestic"].var.asset_target[portfolios[0]] = target

    environment.par.global_parameters['cov_memory'] = 0
    environment.par.global_parameters['conv_bound'] = 0.01


    var = copy.copy(portfolios)
    var.append("FX")

    seed = i
    seed1 = seed

    obj_label = "QE_med_" + str(target) +
    print(i)
    portfolios, currencies, environment, exogenous_agents, funds, data_t = spillover_model(
        portfolios, currencies, environment, exogenous_agents, funds, seed, seed1, obj_label,
        saving_params, var)