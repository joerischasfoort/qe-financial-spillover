import  pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


path = "/Users/Tina/git_repos/qe-financial-spillover/"
path1 = "/Users/Tina/git_repos/QE-server/Objects_Tina_Med/relative/"
import  pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools
from functions.analysis_functions import *


start_day = 2
end_day = 1002

variable =  [0, 100,200,300,400,500, 600]
seeds = [1,2,3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19,20]
variable = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600]
seeds = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

analyze = ["fx", "returns","assets","prices","weights","covariance"]
benchmark = "QE_med_0"



data_mean = {}
data_p5 = {}
data_p95 = {}
data_mean_raw = {}
data_p5_raw = {}
data_p95_raw = {}


for seed in seeds:
    ordered_var_list = []
    for i in variable:
        obj_label = "QE_med_" + str(i)
        obj_label = "QE_Tina_seed" + str(seed) + "_QE" + str(i)

        ordered_var_list.append(obj_label)

    benchmark = "QE_Tina_seed" + str(seed) + "_QE0"

    print(seed)
    filename = path1+ 'Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'

    data = open(filename, "rb")
    list_of_objects = pickle.load(data)
    seedx = list_of_objects[0]
    raw_data = list_of_objects[1]
    relative_data = list_of_objects[2]

    dm, d_p5, d_p95  = compute_averages(relative_data, benchmark, ordered_var_list, range(0,1000))
    dm_raw, d_p5_raw, d_p95_raw  = compute_averages(raw_data, benchmark, ordered_var_list, range(0,1000))

    data_mean.update({seedx: dm})
    data_p5.update({seedx: d_p5})
    data_p95.update({seedx: d_p95})

    data_mean_raw.update({seedx: dm_raw})
    data_p5_raw.update({seedx: d_p5_raw})
    data_p95_raw.update({seedx: d_p95_raw})


MC_mean, MC_p5, MC_p95 =  compute_MCaverages(data_mean, seeds)

MC_mean_raw, MC_p5_raw, MC_p95_raw =  compute_MCaverages(data_mean_raw, seeds)


var = 'funds[0].exp.returns[portfolios[0]]'

#
x_factor = 1
y_factor = 2500000

#
location = 'lower left'
name = 'domestic_bond_return'
saving = 0
plot_conf(var,MC_mean, MC_p5, MC_p95, variable,x_factor,y_factor, location, name, saving)

plt.show()
print 'hello'
#var = 'funds[3].var.assets[portfolios[0]]'
#var = 'funds[2].var.weights[currencies[0]]'
#var = 'funds[3].var.currency[currencies[0]]'
#var = 'funds[2].var.weights[portfolios[0]]'
#
#x_factor = 1
#y_factor = 1
#y_factor = 100/MC_mean_raw[var][0]
#
#location = 'lower left'
#name = 'domestic_bond_return'
#saving = 0
#plot_conf(var,MC_mean_raw, MC_p5_raw, MC_p95_raw, variable,x_factor,y_factor, location, name, saving)


#x=MC_mean["funds[0].var.currency[currencies[0]]"]
#i=np.array(x)/np.array([1,1,2,3,4,5,6])
#res =  np.mean(i[1:])