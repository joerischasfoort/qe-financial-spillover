import  pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools
from analysis_functions import *


start_day = 2
end_day = 1000

variable =  [0, 100,200,300,400,500, 600]
seeds = [1,2,3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19,20]

analyze = ["fx", "returns","assets","prices","weights","covariance",'default_prob']
benchmark = "QE_med_0"


new_data = {}
new_data_raw = {}

ordered_var_list = []
vars = ["funds[0].exp.default_rates[portfolios["+str(a)+"]]" for a in range(4)]
vars.append("funds[0].exp.returns[portfolios[0]]")

for i in variable:
    obj_label = "QE_med_" + str(i)
    ordered_var_list.append(obj_label)
    new_data.update({obj_label: {}})
    new_data_raw.update({obj_label: {}})

    for v in vars:
        new_data[obj_label].update({v:{}})
        new_data_raw[obj_label].update({v:{}})

data_mean = {}
data_p5 = {}
data_p95 = {}
data_mean_raw = {}
data_p5_raw = {}
data_p95_raw = {}



for seed in seeds:

    print(seed)
    filename = 'raw_and_relative_data_seed_' + str(seed) + '.pkl'
    data = open(filename, "rb")
    list_of_objects = pickle.load(data)
    seedx = list_of_objects[0]
    raw_data = list_of_objects[1]
    relative_data = list_of_objects[2]

    for v in new_data:
        for vv in vars:
            new_data[v][vv].update({seed:relative_data[v][vv]})
            new_data_raw[v][vv].update({seed:raw_data[v][vv]})

daily_data = {}
for v in new_data:
    daily_data.update({v:{}})
    for vv in vars:
        daily_data[v].update({vv:[]})
        for t in range(len(new_data[v][vv][1])):
            daily_data[v][vv].append(np.mean([new_data[v][vv][seed][t] for seed in seeds]))





