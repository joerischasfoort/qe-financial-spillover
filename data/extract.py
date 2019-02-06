
import  pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


path = "/Users/Tina/git_repos/QE-server/Objects_Tina_Med/relative/"

var_list_all = ['funds[3].exp.returns[currencies[0]]', # domestic currency
            'funds[0].exp.returns[currencies[1]]',  # foreign currency
            'funds[0].exp.returns[portfolios[0]]',   # domestic bond
            'funds[0].exp.returns[portfolios[1]]',  #  domestic equity
            'funds[3].exp.returns[portfolios[2]]',   # foreign bond
            'funds[3].exp.returns[portfolios[3]]',  #  foreign equity
                ]

seeds = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
#
# #### GET all the with the next code (14 x 1000 x 20)
df = pd.DataFrame()
df_list = []

for seed in seeds:
    filename = path + 'Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'
    data = open(filename, "rb")
    list_of_objects = pickle.load(data)
    seedx = list_of_objects[0]
    raw_data = list_of_objects[1]
    relative_data = list_of_objects[2]
    print seed

    rows = []
    for qe, assets in relative_data.items():
        all = {}
        #
        for key_asset, var in assets.items():
            if key_asset in var_list_all:

                for time, val in enumerate(var):
                    all = {}
                    all['seed'] = seed

                    list_temp = []
                    list_temp.append(qe)

                    #print list_temp[0][qe.find('_', 10):] This drags out the QE

                    all['QE'] = list_temp[0][qe.find('_', 10) + 3:]
                    all['asset'] = key_asset
                    all['val'] = val
                    all['time'] = time
                    print time
                    rows.append(all)

    temp = pd.DataFrame(rows) # all times per experiment
    df_list.append(temp) # all data per seed
df1 = pd.concat(df_list, keys=[2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])  # concat seeds
Delete first column:
df1.to_csv('test6.csv')

 
df_long.to_csv('yields.csv')
 




