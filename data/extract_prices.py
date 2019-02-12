
import  pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


path = "/Users/Tina/git_repos/QE-server/Objects_Tina_Med/relative/"


seeds = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
#
# #### GET all the with the next code (14 x 1000 x 20)
df = pd.DataFrame()
df_list = []

var_list_price = [ 'percentage_portfolio2', 'percentage_portfolio1',
                   'percentage_portfolio0' ,'percentage_fx_rates.iloc[0,1]', 'percentage_portfolio3' ]

for seed in seeds:
    filename = path + 'Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'
    data = open(filename, "rb")
    list_of_objects = pickle.load(data)
    seedx = list_of_objects[0]
    raw_data = list_of_objects[1]
    relative_data = list_of_objects[2]

    for key, value in relative_data.items():
        relative_data[key]['percentage_portfolio2'] = relative_data[key]['portfolios[2].var.price'] / \
                                                      raw_data['QE_Tina_seed' + str(seed) + '_QE0'][
                                                          'portfolios[2].var.price'] * 100
        relative_data[key]['percentage_portfolio1'] = relative_data[key]['portfolios[1].var.price'] / \
                                                      raw_data['QE_Tina_seed' + str(seed) + '_QE0'][
                                                          'portfolios[1].var.price'] * 100
        relative_data[key]['percentage_portfolio0'] = relative_data[key]['portfolios[0].var.price'] / \
                                                      raw_data['QE_Tina_seed' + str(seed) + '_QE0'][
                                                          'portfolios[0].var.price'] * 100
        relative_data[key]['percentage_portfolio3'] = relative_data[key]['portfolios[3].var.price'] / \
                                                      raw_data['QE_Tina_seed' + str(seed) + '_QE0'][
                                                          'portfolios[3].var.price'] * 100

        relative_data[key]['percentage_fx_rates.iloc[0,1]'] = relative_data[key]['environment.var.fx_rates.iloc[0,1]'] / \
                                                              raw_data['QE_Tina_seed' + str(seed) + '_QE0'][
                                                                  'environment.var.fx_rates.iloc[0,1]'] * 100

    rows = []

    for qe, assets in relative_data.items():
        all = {}
        #
        for key_asset, var in assets.items():
            if key_asset in var_list_price:

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

df1.to_csv('prices_long.csv')

 

 




