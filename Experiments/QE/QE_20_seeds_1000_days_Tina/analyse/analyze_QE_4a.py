import  pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools
from analysis_functions import *


start_day = 2
end_day = 1000


variable = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600]
#20seeds
seeds = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]


analyze = ["fx", "returns","assets","prices","weights","covariance",'default_prob']
benchmark = "QE_med_0"


local_dir = "Z:\Objects_QE_med/"
#local_dir = "Objects_QE_1pcfxs/"

filename = local_dir + "objects_day_2_seed_1_QE_med_0.pkl"
data = open(filename, "rb")
list_of_objects = pickle.load(data)

portfolios = list_of_objects[0]
currencies = list_of_objects[1]
environment = list_of_objects[2]
exogeneous_agents = list_of_objects[3]
funds = list_of_objects[4]



for seed in seeds:

    raw_data = {}
    ordered_var_list = []
    for i in variable:
        obj_label =  "QE_med_" + str(i)
        ordered_var_list.append(obj_label)
        raw_data.update({obj_label: creating_lists(analyze, funds, portfolios,currencies, environment,exogeneous_agents)})

        for day in range(start_day,end_day+1):
            print(i, seed, day)

            filename = local_dir + "objects_day_" + str(day) + "_seed_"+str(seed)+"_"  + obj_label+".pkl"
            data = open(filename,"rb")
            list_of_objects = pickle.load(data)

            portfolios = list_of_objects[0]
            currencies = list_of_objects[1]
            environment = list_of_objects[2]
            exogeneous_agents = list_of_objects[3]
            funds = list_of_objects[4]

            raw_data[obj_label] = add_observations( raw_data[obj_label], funds, portfolios,currencies, environment,exogeneous_agents)


    relative_data =  relative_development(raw_data, benchmark)

    data_mean, data_p5, data_p95  = compute_averages(relative_data,benchmark, ordered_var_list, range(900,999))

    file_name = 'raw_and_relative_data_seed_' + str(seed) + '.pkl'
    save_objects = open(file_name, 'wb')
    list_of_objects = [seed, raw_data, relative_data]
    pickle.dump(list_of_objects, save_objects)
    save_objects.close()


    var = 'funds[0].exp.returns[portfolios[0]]'
    #var = "environment.var.fx_rates.iloc[0,1]"
    x_factor = 1
    y_factor = 250*100*100
    #y_factor = 1
    location = 'lower left'
    name = 'domestic_bond_return'
    saving = 0
  #  plot_conf(var,data_mean, data_p5, data_p95, variable,x_factor,y_factor, location, name, saving)



