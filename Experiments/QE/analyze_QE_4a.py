import  pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools
from analysis_functions import *


start_day = 2
end_day = 1000

variable = [0, 200]
analyze = ["fx", "returns"]
benchmark = "QE_0"


local_dir = "C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects/"
#local_dir = "Objects_QE_1pcfxs/"

filename = local_dir + "objects_day_" + str(2) + "_seed_1_" + "QE_0" + ".pkl"
data = open(filename, "rb")
list_of_objects = pickle.load(data)

portfolios = list_of_objects[0]
currencies = list_of_objects[1]
environment = list_of_objects[2]
exogeneous_agents = list_of_objects[3]
funds = list_of_objects[4]





raw_data = {}
for i in variable:
    obj_label =  "QE_" + str(i)
    raw_data.update({obj_label: creating_lists(analyze, funds, portfolios,currencies, environment,exogeneous_agents)})

    for day in range(start_day,end_day+1):
        filename = local_dir + "objects_day_" + str(day) + "_seed_1_"  + obj_label+".pkl"
        data = open(filename,"rb")
        list_of_objects = pickle.load(data)

        portfolios = list_of_objects[0]
        currencies = list_of_objects[1]
        environment = list_of_objects[2]
        exogeneous_agents = list_of_objects[3]
        funds = list_of_objects[4]

        raw_data[obj_label] = add_observations( raw_data[obj_label], funds, portfolios,currencies, environment,exogeneous_agents)


relative_data =  relative_development(raw_data, benchmark)

