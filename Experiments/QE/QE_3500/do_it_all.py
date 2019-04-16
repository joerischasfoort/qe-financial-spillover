
import  pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.append('/scratch/kzltin001/qe-financial-spillover')

local_dir = "/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_3500/Med_3500/raw_relative/"



var_list_returns = ['funds[3].exp.returns[currencies[0]]', # domestic currency
            'funds[0].exp.returns[currencies[1]]',  # foreign currency
            'funds[0].exp.returns[portfolios[0]]',   # domestic bond
            'funds[0].exp.returns[portfolios[1]]',  #  domestic equity
            'funds[3].exp.returns[portfolios[2]]',   # foreign bond
            'funds[3].exp.returns[portfolios[3]]',  #  foreign equity
                ]

var_list_price = [ 'percentage_portfolio2', 'percentage_portfolio1',
                   'percentage_portfolio0' ,'percentage_fx_rates.iloc[0,1]', 'percentage_portfolio3' ]





#20seeds
seeds = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
#5 and 7 did not work
seeds = [2, 3, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
#
# #### GET all the with the next code (14 x 1000 x 20)
df = pd.DataFrame()
df_list = []

print('############# Reading bond and equity returns..########')
for seed in seeds:
    filename = local_dir + '3500_Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'
    data = open(filename, "rb")
    list_of_objects = pickle.load(data)
    seedx = list_of_objects[0]
    raw_data = list_of_objects[1]
    relative_data = list_of_objects[2]
    print seed, 'returns data'

    rows = []

    for qe, assets in relative_data.items():
        all = {}
        #
        for key_asset, var in assets.items():
            if key_asset in var_list_returns:
                #print key_asset
                for time, val in enumerate(var):
                    all = {}
                    all['seed'] = seed

                    list_temp = []
                    list_temp.append(qe)

                    #print list_temp[0][qe.find('_', 10):] This drags out the QE

                    all['QE'] = list_temp[0][qe.find('_', 15) + 3:]
                    all['asset'] = key_asset
                    all['val'] = val
                    all['time'] = time
                    #print time
                    rows.append(all)

    temp = pd.DataFrame(rows) # all times per experiment
    df_list.append(temp) # all data per seed
df_exp_returns = pd.concat(df_list, keys=seeds , sort=True)  # concat seeds
########################################################################
########################################################################
########################################################################

'''
Remember that I multiply by 100!!!!!!!!!!!!!!
'''
df = pd.DataFrame()
df_list = []

var_list_price = [ 'percentage_portfolio2', 'percentage_portfolio1',
                   'percentage_portfolio0' ,'percentage_fx_rates.iloc[0,1]', 'percentage_portfolio3' ]
print('############# Reading prices..########')
for seed in seeds:
    filename = local_dir + '3500_Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'
    data = open(filename, "rb")
    list_of_objects = pickle.load(data)
    seedx = list_of_objects[0]
    raw_data = list_of_objects[1]
    relative_data = list_of_objects[2]
    print seed, 'PRICES data'
    for key, value in relative_data.items():
        relative_data[key]['percentage_portfolio2'] = relative_data[key]['portfolios[2].var.price'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Tina_3500med_QE0'][
                                                          'portfolios[2].var.price'] * 100
        relative_data[key]['percentage_portfolio1'] = relative_data[key]['portfolios[1].var.price'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Tina_3500med_QE0'][
                                                          'portfolios[1].var.price'] * 100
        relative_data[key]['percentage_portfolio0'] = relative_data[key]['portfolios[0].var.price'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Tina_3500med_QE0'][
                                                          'portfolios[0].var.price'] * 100
        relative_data[key]['percentage_portfolio3'] = relative_data[key]['portfolios[3].var.price'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Tina_3500med_QE0'][
                                                          'portfolios[3].var.price'] * 100

        relative_data[key]['percentage_fx_rates.iloc[0,1]'] = relative_data[key]['environment.var.fx_rates.iloc[0,1]'] / \
                                                              raw_data['_seed_' +str(seed)  + '_Tina_3500med_QE0'][
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

                    all['QE'] = list_temp[0][qe.find('_', 15) + 3:]
                    all['asset'] = key_asset
                    all['val'] = val
                    all['time'] = time
                    #print time
                    rows.append(all)

    temp = pd.DataFrame(rows) # all times per experiment
    df_list.append(temp) # all data per seed
df_prices = pd.concat(df_list, keys=seeds,  sort=True)  # concat seeds



########################################################################
########################################################################
########################################################################
var_list_asset = [
        'funds[0].var.assets[portfolios[0]]'  ,
        'funds[0].var.assets[portfolios[1]]' ,
        'funds[0].var.assets[portfolios[2]]',
        'funds[0].var.assets[portfolios[3]]',
        'funds[0].var.currency[currencies[0]]',
        'funds[0].var.currency[currencies[1]]',
        'funds[1].var.assets[portfolios[0]]'  ,
        'funds[1].var.assets[portfolios[1]]' ,
        'funds[1].var.assets[portfolios[2]]',
        'funds[1].var.assets[portfolios[3]]',
        'funds[1].var.currency[currencies[0]]',
        'funds[1].var.currency[currencies[1]]',

        'funds[2].var.assets[portfolios[0]]' ,
        'funds[2].var.assets[portfolios[1]]' ,
        'funds[2].var.assets[portfolios[2]]',
        'funds[2].var.assets[portfolios[3]]',
        'funds[2].var.currency[currencies[0]]',
        'funds[2].var.currency[currencies[1]]',

        'funds[3].var.assets[portfolios[0]]' ,
        'funds[3].var.assets[portfolios[1]]' ,
        'funds[3].var.assets[portfolios[2]]',
        'funds[3].var.assets[portfolios[3]]',
        'funds[3].var.currency[currencies[0]]',
         'funds[3].var.currency[currencies[1]]',
         ] 
 


df = pd.DataFrame()
df_list = []

# Let's go get the asset holding after QE is implemented (we only need first observations)
print('############# Reading asset holdings..########')
for seed in seeds:
    filename = local_dir + '3500_Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'
    data = open(filename, "rb")
    list_of_objects = pickle.load(data)
    seedx = list_of_objects[0]
    raw_data = list_of_objects[1]
    relative_data = list_of_objects[2]
    print seed,    'asset holding data'
        # Add a variable for percentage changes in asset holdings

    rows = []

    for key, value in raw_data.items():
         for k2, v2 in value.items():
              value[k2] = v2[0]

    for key, value in relative_data.items():
        for k2, v2 in value.items():
            value[k2] = v2[0]

    for key, value in relative_data.items():
            # creates keys in dictionary for percentage changes 
        for va in var_list_asset:
            relative_data[key]['percentage_assets'+va] = \
                relative_data[key][va] / raw_data['_seed_' +str(seed)  + '_Tina_3500med_QE0'][va] * 100

                 
    for qe, assets in relative_data.items():
        # all = {}
        
        for key_asset, var in assets.items():


            if key_asset in var_list_asset:
                #print var, key_asset
            #     print key_asset

                all = {}
                all['seed'] = seed

                list_temp = []
                list_temp.append(qe)

                    #print list_temp[0][qe.find('_', 10):] This drags out the QE

                all['QE'] = list_temp[0][qe.find('_', 13) + 3:]
                all['asset'] = key_asset
                all['val'] = var
                all['time'] = 1

                rows.append(all)

    temp = pd.DataFrame(data=rows)

    df_list.append(temp)
df_assets = pd.concat(df_list, keys=seeds,  sort=True)  # use seeds!


#saving 
df_assets.to_csv('df_assets.csv') 
df_prices.to_csv('df_prices.csv')
df_exp_returns.to_csv('df_exp_returns.csv')
df_assets.to_pickle('df_assets.pickle')
df_prices.to_pickle('df_prices.pickle')
df_exp_returns.to_pickle('df_exp_returns.pickle')
#df_assets = pd.read_csv(local_dir+'df_assets.csv') 
# df_prices= pd.read_pickle(local_dir+'df_prices.pickle')
# df_exp_returns = pd.read_pickle(local_dir+'df_exp_returns.pickle')

df_list = [ df_prices, df_exp_returns ] 
df_final = pd.concat(df_list, keys=['prices', 'returns'])  # concat seeds
df_final = df_final.iloc[:, 0:]
df_final = df_final.pivot_table(columns=['asset'], index=['QE', 'seed', 'time'], values='val')

df_final.to_csv('df_final.csv')
