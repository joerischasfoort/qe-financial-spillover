import  pickle
from spillover_model_cb import *
import time


bounds = [0.1,0.09,0.07,0.05,0.03,0.009,0.007,0.005,0.003,0.01,0.001,0.0001,0.00001,0.000001,0.0000001,0.00000001]


for i in bounds:


    data = open('Objects_CB/CALIBRATED_MASTER_MED.pkl', 'rb')

    list_of_objects = pickle.load(data)

    portfolios = list_of_objects[0]
    currencies = list_of_objects[1]
    environment = list_of_objects[2]
    exogenous_agents = list_of_objects[3]
    funds = list_of_objects[4]
    seed = list_of_objects[5]
    obj_label = list_of_objects[6]

    data.close()

    environment.par.global_parameters["start_day"]=2
    environment.par.global_parameters["end_day"]=201

    saving_params = {}
    #saving_params.update({"path": '/home/jriedler/qe-financial-spillover/Experiments/QE/Objects'})
    saving_params.update({"path": 'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects'})
    saving_params.update({"time": 100})


    environment.par.global_parameters['cov_memory'] = 0
    environment.par.global_parameters['conv_bound'] = i

    obj_label=str(i)

    var = copy.copy(portfolios)
    var.append("FX")

    seed1 = seed



    start = time.time()
    portfolios, currencies, environment, exogenous_agents, funds, data_t = spillover_model_cb(
        portfolios, currencies, environment, exogenous_agents, funds, seed, seed1, obj_label,
        saving_params, var)
    end = time.time()
    print(i, end - start)
