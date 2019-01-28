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
var = 'funds[0].exp.returns[portfolios[0]]'
for e in experiments:
    benchmark = e+"6.25"




    ordered_var_list = []
    for i in variable:
        obj_label = e + str(i)
        ordered_var_list.append(obj_label)






    locals()[e+"data_mean_raw"] = {o:[] for o in ordered_var_list}
    locals()[e+"data_p5_raw" ] = {o:[] for o in ordered_var_list}
    locals()[e+"data_p95_raw" ] = {o:[] for o in ordered_var_list}

    locals()[e+"mean_raw"] = {o:{} for o in ordered_var_list}
    locals()[e+"p5_raw" ] = {o:{} for o in ordered_var_list}
    locals()[e+"p95_raw" ] = {o:{} for o in ordered_var_list}

    MC_mean_raw = {o:[] for o in ordered_var_list}
    MC_p5_raw = {o:[] for o in ordered_var_list}
    MC_p95_raw = {o:[] for o in ordered_var_list}

    for seed in seeds:
        print(seed)
        filename = 'raw_and_relative_data_' + e + 'seed_' + str(seed) + '.pkl'
        data = open(filename, "rb")
        list_of_objects = pickle.load(data)
        seedx = list_of_objects[0]
        raw_data = list_of_objects[1]
        relative_data = list_of_objects[2]

        dm_raw, d_p5_raw, d_p95_raw  = compute_averages(raw_data, benchmark, ordered_var_list, range(0,999))


        for i, o in enumerate(ordered_var_list):
            locals()[e+"data_mean_raw"][o].append(dm_raw[var][i])
            locals()[e+"data_p5_raw" ][o].append(d_p5_raw[var][i])
            locals()[e+"data_p95_raw" ][o].append(d_p95_raw[var][i])

        for i, o in enumerate(ordered_var_list):
            locals()[e+"mean_raw"][o].update({seed:dm_raw[var][i]})
            locals()[e+"p5_raw" ][o].update({seed:d_p5_raw[var][i]})
            locals()[e+"p95_raw" ][o].update({seed:d_p95_raw[var][i]})


for e in experiments:
    ordered_var_list = []
    for i in variable:
        obj_label = e + str(i)
        ordered_var_list.append(obj_label)

    for o in ordered_var_list:
        MC_mean_raw[o] = np.mean(np.array(locals()[e+"data_mean_raw"][o]))
        MC_p5_raw[o] = np.mean(np.array(locals()[e+"data_p5_raw"][o]))
        MC_p95_raw[o] = np.mean(np.array(locals()[e+"data_p95_raw"][o]))

        file_name = e+'MC_means.pkl'
        save_objects = open(file_name, 'wb')
        list_of_objects = [MC_mean_raw, MC_p5_raw, MC_p95_raw]
        pickle.dump(list_of_objects, save_objects)
        save_objects.close()


for seed in seeds:
    print(seed)
    for e in experiments:
        filename = 'raw_and_relative_data_' + e + 'seed_' + str(seed) + '.pkl'
        data = open(filename, "rb")
        list_of_objects = pickle.load(data)
        seedx = list_of_objects[0]
        locals()[e+'raw'] = list_of_objects[1]
        relative_data = list_of_objects[2]



