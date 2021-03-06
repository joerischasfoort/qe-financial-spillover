
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


for seed in seeds:
    filename = path + 'Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'
    data = open(filename, "rb")
    list_of_objects = pickle.load(data)
    seedx = list_of_objects[0]
    raw_data = list_of_objects[1]
    relative_data = list_of_objects[2]
    print seed
        # Add a variable for percentage changes in asset holdings

    rows = []

    for key, value in raw_data.items():
         for k2, v2 in value.items():
              value[k2] = v2[0]

    for key, value in relative_data.items():
        for k2, v2 in value.items():
            value[k2] = v2[0]

    for key, value in relative_data.items():
            # assets for funds
        for va in var_list_asset:
            relative_data[key]['percentage_assets'+va] = \
                relative_data[key][va] / raw_data['QE_Tina_seed' + str(seed) + '_QE0'][va] * 100


    for qe, assets in relative_data.items():
        # all = {}
        #
        for key_asset, var in assets.items():


            if key_asset in var_list_asset:
                print var, key_asset
            #     print key_asset

                all = {}
                all['seed'] = seed

                list_temp = []
                list_temp.append(qe)

                    #print list_temp[0][qe.find('_', 10):] This drags out the QE

                all['QE'] = list_temp[0][qe.find('_', 10) + 3:]
                all['asset'] = key_asset
                all['val'] = var
                all['time'] = 1

                rows.append(all)

    temp = pd.DataFrame(data=rows)

    df_list.append(temp)

df1_assets = pd.concat(df_list, keys=[1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])  # use seeds!

#df1_assets.to_csv('test_assets_holdings.csv')





