
import  pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


sys.path.append('/Users/Tina/git_repos/qe-financial-spillover/')
from functions.helper import read_data


"Important, this must be the same as from analyze that was run before - More elegant solution?"

experiment_dir = "/Users/Tina/git_repos/qe-financial-spillover/Experiments/QE/QE_2500_2750/"
outputfolder = 'raw_relative/test/'
pickl_dir = experiment_dir + outputfolder

output = experiment_dir + 'df_final.csv'

assets_target = [0, 100, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600]
seeds = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]


 
var_list_returns = ['funds[3].exp.returns[currencies[0]]', # domestic currency
            'funds[0].exp.returns[currencies[1]]',  # foreign currency
            'funds[0].exp.returns[portfolios[0]]',   # domestic bond
            'funds[0].exp.returns[portfolios[1]]',  #  domestic equity
            'funds[3].exp.returns[portfolios[2]]',   # foreign bond
            'funds[3].exp.returns[portfolios[3]]',  #  foreign equity
                ]
var_list_price = [ 'percentage_portfolio2', 'percentage_portfolio1',
                   'percentage_portfolio0' ,'percentage_fx_rates.iloc[0,1]', 'percentage_portfolio3' ]


var_list = list(set(var_list_returns + var_list_price))

label_zero = "_2500_2750_med_QE0"


"We need file_name - file_name at the end of make_relative_data check() in helper -- More elegant solution??! "
" e.g  file_name = pickl_dir +'Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'   "
important_filelabel = '_2500_2750_med_QETina_raw_and_relative_data_seed_'


df = read_data(pickl_dir, seeds, important_filelabel, var_list, label_zero)


# Dataframe handling

df_final = df.pivot_table(columns=['asset'], index=['QE', 'seed', 'time'], values='val')


df_final.to_csv(output)
# df_final = df_final.iloc[:, 3:] ???

print("Data was saved in" +  output + " Happy analysing!")


# df_list = [ df_prices, df_exp_returns ] 

# df_final = pd.concat(df_list, keys=['prices', 'returns'])  # concat seeds
# df_final = df_final.iloc[:, 3:]

  
# Remember that I multiply by 100!!!!!!!!!!!!!!
 
# ########################################################################
# var_list_asset = [
#         'funds[0].var.assets[portfolios[0]]'  ,
#         'funds[0].var.assets[portfolios[1]]' ,
#         'funds[0].var.assets[portfolios[2]]',
#         'funds[0].var.assets[portfolios[3]]',
#         'funds[0].var.currency[currencies[0]]',
#         'funds[0].var.currency[currencies[1]]',
#         'funds[1].var.assets[portfolios[0]]'  ,
#         'funds[1].var.assets[portfolios[1]]' ,
#         'funds[1].var.assets[portfolios[2]]',
#         'funds[1].var.assets[portfolios[3]]',
#         'funds[1].var.currency[currencies[0]]',
#         'funds[1].var.currency[currencies[1]]',

#         'funds[2].var.assets[portfolios[0]]' ,
#         'funds[2].var.assets[portfolios[1]]' ,
#         'funds[2].var.assets[portfolios[2]]',
#         'funds[2].var.assets[portfolios[3]]',
#         'funds[2].var.currency[currencies[0]]',
#         'funds[2].var.currency[currencies[1]]',

#         'funds[3].var.assets[portfolios[0]]' ,
#         'funds[3].var.assets[portfolios[1]]' ,
#         'funds[3].var.assets[portfolios[2]]',
#         'funds[3].var.assets[portfolios[3]]',
#         'funds[3].var.currency[currencies[0]]',
#          'funds[3].var.currency[currencies[1]]',
#          ] 
 


# df = pd.DataFrame()
# df_list = []

# # Let's go get the asset holding after QE is implemented (we only need first observations)
# print('############# Reading asset holdings..########')
# for seed in seeds:
#     filename = local_dir + 'med_25002750_Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'
#     data = open(filename, "rb")
#     list_of_objects = pickle.load(data)
#     seedx = list_of_objects[0]
#     raw_data = list_of_objects[1]
#     relative_data = list_of_objects[2]
#     print seed,    'asset holding data'
#         # Add a variable for percentage changes in asset holdings

#     rows = []

#     for key, value in raw_data.items():
#          for k2, v2 in value.items():
#               value[k2] = v2[0]

#     for key, value in relative_data.items():
#         for k2, v2 in value.items():
#             value[k2] = v2[0]

#     for key, value in relative_data.items():
#             # creates keys in dictionary for percentage changes 
#         for va in var_list_asset:
#             relative_data[key]['percentage_assets'+va] = \
#                 relative_data[key][va] / raw_data['_seed_' +str(seed)  + '_2500_2750_med_QE0'][va] * 100

                 
#     for qe, assets in relative_data.items():
#         # all = {}
        
#         for key_asset, var in assets.items():


#             if key_asset in var_list_asset:
#                 #print var, key_asset
#             #     print key_asset

#                 all = {}
#                 all['seed'] = seed

#                 list_temp = []
#                 list_temp.append(qe)

#                     #print list_temp[0][qe.find('_', 10):] This drags out the QE

#                 all['QE'] = list_temp[0][qe.find('_', 15) + 3:]
#                 all['asset'] = key_asset
#                 print var
#                 all['val'] = var
#                 all['time'] = 1

#                 rows.append(all)

#     temp = pd.DataFrame(data=rows)

#     df_list.append(temp)
# df_assets = pd.concat(df_list, keys=seeds,  sort=True)  # use seeds!



