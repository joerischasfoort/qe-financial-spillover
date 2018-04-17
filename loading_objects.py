import  pickle
from spillover_model import *

data = open('data/Objects/objects_day_45.pkl', 'rb')

list_of_objects = pickle.load(data)

portfolios = list_of_objects[0]
currencies = list_of_objects[1]
environment = list_of_objects[2]
exogeneous_agents = list_of_objects[3]
funds = list_of_objects[4]
seed = list_of_objects[5]

data.close()

environment.par.global_parameters["start_day"]=1000
environment.par.global_parameters["end_day"]=3000


portfolios, currencies, environment, exogeneous_agents, funds, data_t = spillover_model(portfolios, currencies, environment, exogeneous_agents, funds,  seed=1)
