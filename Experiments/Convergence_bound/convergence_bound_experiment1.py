import  pickle
from spillover_model_CB1 import *
import time


bounds = [0.1,0.09,0.07,0.05,0.03,0.009,0.007,0.005,0.003,0.01,0.001,0.0001,0.00001,0.000001,0.0000001,0.00000001]


for i in bounds:


    data = open('Objects_CB1/objects_day_4999_seed_1_fx_rev_speed_0.14.pkl', 'rb')

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
    environment.par.global_parameters["end_day"]=5249


    obj_label=str(i)
    environment.par.global_parameters["convergence_bound"] = i
    start = time.time()
    portfolios, currencies, environment, exogeneous_agents, funds, data_t = spillover_model_CB1(portfolios, currencies, environment, exogeneous_agents, funds,  seed, obj_label)
    end = time.time()
    print(i, end - start)
