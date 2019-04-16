
import  pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


path = "/Users/Tina/git_repos/qe-financial-spillover/Experiments/QE/QE_10days/relative/"


seeds = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]


df = pd.DataFrame()
df_list = []

var_list_price = [ 'percentage_portfolio2', 'percentage_portfolio1',
                   'percentage_portfolio0' ,'percentage_fx_rates.iloc[0,1]', 'percentage_portfolio3' ]

for seed in seeds:
    filename = path + '10days_Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'
    data = open(filename, "rb")
    list_of_objects = pickle.load(data)
    seedx = list_of_objects[0]
    raw_data = list_of_objects[1]
    relative_data = list_of_objects[2]

    for key, value in relative_data.items():

        relative_data[key]['percentage_portfolio2'] = relative_data[key]['portfolios[2].var.price'] / \
                                                      raw_data['_seed_' + str(seed) + '_Tina_10days_QE0'][
                                                          'portfolios[2].var.price'] * 100
        relative_data[key]['percentage_portfolio1'] = relative_data[key]['portfolios[1].var.price'] / \
                                                      raw_data['_seed_' + str(seed) + '_Tina_10days_QE0'][
                                                          'portfolios[1].var.price'] * 100
        relative_data[key]['percentage_portfolio0'] = relative_data[key]['portfolios[0].var.price'] / \
                                                      raw_data['_seed_' + str(seed) + '_Tina_10days_QE0'][
                                                          'portfolios[0].var.price'] * 100
        relative_data[key]['percentage_portfolio3'] = relative_data[key]['portfolios[3].var.price'] / \
                                                      raw_data['_seed_' + str(seed) + '_Tina_10days_QE0'][
                                                          'portfolios[3].var.price'] * 100

        relative_data[key]['percentage_fx_rates.iloc[0,1]'] = relative_data[key]['environment.var.fx_rates.iloc[0,1]'] / \
                                                              raw_data['_seed_' + str(seed) + '_Tina_10days_QE0'][
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

                    all['QE'] = list_temp[0][qe.find('_', 16) + 3:]
                    all['asset'] = key_asset
                    all['val'] = val
                    all['time'] = time
                    print time
                    rows.append(all)

    temp = pd.DataFrame(rows) # all times per experiment
    df_list.append(temp) # all data per seed
df1 = pd.concat(df_list, keys=[2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])  # ATTENTION: LIKELY ERROR SOURCE! use CORRECT seeds!# concat seeds

#df1.to_csv('prices_long_10days.csv')

 

 




