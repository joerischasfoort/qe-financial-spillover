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
analyze = ["returns","prices"]
experiments = ["MATwQE_med_", "MAT_med_"]

for e in experiements:
    benchmark = e+"_6.25"




    ordered_var_list = []
    for i in variable:
        obj_label = e + str(i)
        ordered_var_list.append(obj_label)




    data_mean = {}
    data_p5 = {}
    data_p95 = {}
    data_mean_raw = {}
    data_p5_raw = {}
    data_p95_raw = {}


    for seed in seeds:
        print(seed)
        file_name = 'raw_and_relative_data_' + e + 'seed_' + str(seed) + '.pkl'
        data = open(filename, "rb")
        list_of_objects = pickle.load(data)
        seedx = list_of_objects[0]
        raw_data = list_of_objects[1]
        relative_data = list_of_objects[2]

        dm, d_p5, d_p95  = compute_averages(relative_data, benchmark, ordered_var_list, range(0,999))
        dm_raw, d_p5_raw, d_p95_raw  = compute_averages(raw_data, benchmark, ordered_var_list, range(0,999))

        data_mean.update({seedx: dm})
        data_p5.update({seedx: d_p5})
        data_p95.update({seedx: d_p95})

        data_mean_raw.update({seedx: dm_raw})
        data_p5_raw.update({seedx: d_p5_raw})
        data_p95_raw.update({seedx: d_p95_raw})

    MC_mean_raw, MC_p5_raw, MC_p95_raw =  compute_MCaverages(data_mean_raw, seeds)
    file_name = 'MC_means_' + e + '.pkl'
    save_objects = open(file_name, 'wb')
    list_of_objects = [MC_mean_raw, MC_p5_raw, MC_p95_raw]
    pickle.dump(list_of_objects, save_objects)
    save_objects.close()





