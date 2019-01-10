import  pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools
from analysis_functions import *


start_day = 2
end_day = 1000

variable =  [0.08,0.5,1,2,4,6.25,8,10,12,14,16,18,20,30,40]
seeds = [1,2,3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
analyze = ["returns"]


#local_dir = "Objects_QE_1pcfxs/"

filename = "Z:\Objects_MAT_med\CALIBRATED_MASTER_MED.pkl"
data = open(filename, "rb")
list_of_objects = pickle.load(data)

portfolios = list_of_objects[0]
currencies = list_of_objects[1]
environment = list_of_objects[2]
exogeneous_agents = list_of_objects[3]
funds = list_of_objects[4]

experiments = ['MATwQE_med_' "MAT_med_"]


for seed in seeds:
    for e in experiments:
        local_dir = "Z:\Objects_"+e[:-1]+'_MC'+"/"
        local_dir = "C:\Users\jrr\Desktop\Objects_"+e[:-1]+'_MC'+"/"

        raw_data = {}
        ordered_var_list = []
        for i in variable:
            print(i,seed)
            obj_label =  e +str(i)
            ordered_var_list.append(obj_label)
            raw_data.update({obj_label: creating_lists(analyze, funds, portfolios,currencies, environment,exogeneous_agents)})

            for day in range(start_day,end_day+1):
                filename = local_dir + "objects_day_" + str(day) + "_seed_"+str(seed)+"_"  + obj_label+".pkl"
                data = open(filename,"rb")
                list_of_objects = pickle.load(data)

                portfolios = list_of_objects[0]
                currencies = list_of_objects[1]
                environment = list_of_objects[2]
                exogeneous_agents = list_of_objects[3]
                funds = list_of_objects[4]

                raw_data[obj_label] = add_observations( raw_data[obj_label], funds, portfolios,currencies, environment,exogeneous_agents)

        benchmark = e+"6.25"

        relative_data =  relative_development2(raw_data, benchmark)


        file_name = 'raw_and_relative_data_'+e+'seed_' + str(seed) + '.pkl'
        save_objects = open(file_name, 'wb')
        list_of_objects = [seed, raw_data, relative_data]
        pickle.dump(list_of_objects, save_objects)
        save_objects.close()

    #data_mean, data_p5, data_p95 = compute_averages(raw_data, benchmark, ordered_var_list, range(0, 999))
    #
    #var = 'funds[0].exp.returns[portfolios[0]]'
    ##var = "environment.var.fx_rates.iloc[0,1]"
    #x_factor = 1
    #y_factor = 250*100
    ##y_factor = 1
    #location = 'lower left'
    #name = 'domestic_bond_return'
    #saving = 0
    #plot_conf(var,data_mean, data_p5, data_p95, variable,x_factor,y_factor, location, name, saving)
    #
    #

