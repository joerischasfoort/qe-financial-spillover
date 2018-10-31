import  pickle
from spillover_model import *

data = open('data/Objects/objects_day_1690_seed_1_4ax.pkl', 'rb')
#data = open('data/Objects/objects_nonConv_day8890.pkl', 'rb')

list_of_objects = pickle.load(data)

portfolios = list_of_objects[0]
currencies = list_of_objects[1]
environment = list_of_objects[2]
exogenous_agents = list_of_objects[3]
funds = list_of_objects[4]
seed = list_of_objects[5]
obj_label = list_of_objects[6]

data.close()

environment.par.global_parameters["start_day"]=1691
environment.par.global_parameters["end_day"]=5001


saving_params = {}
saving_params.update({"path": 'C:\Users\jrr\Documents\GitHub\qe-financial-spillover\data\Objects'})
saving_params.update({"time": 0})


portfolios, currencies, environment, exogenous_agents, funds, data_t = spillover_model(portfolios, currencies, environment, exogenous_agents, funds, seed, obj_label, saving_params)

