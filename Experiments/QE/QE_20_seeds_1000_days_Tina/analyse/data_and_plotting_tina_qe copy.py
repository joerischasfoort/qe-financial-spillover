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
            'environment.var.fx_rates.iloc[0,1]', #  exchange rate   funds[0].var.covariance_matrix.iloc[0,2]
            'portfolios[0].var.price',
            'portfolios[1].var.price',
            'portfolios[2].var.price',
            'portfolios[3].var.price',
            'percentage_portfolio2',
            'percentage_portfolio0',
            'percentage_portfolio3',
            'percentage_portfolio1',
            'percentage_forex',
                ]

var_list_asset_positions = \
              [
            'funds[0].exp.returns[portfolios[0]]',   # domestic bond - leave to test later
            "funds[0].var.covariance_matrix.iloc[0,0]" , # domestic bond
            "funds[0].var.covariance_matrix.iloc[1,1]" , # domestic equity
            "funds[0].var.covariance_matrix.iloc[2,2]" , #  foreign bond
            "funds[0].var.covariance_matrix.iloc[3,3]" , # foreign equity
            'percentage_var1',
            'percentage_var2',
            'percentage_var0',
            'percentage_var3'
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

    # for key, value in relative_data.items():
    #     relative_data[key]['percentage_var2'] = relative_data[key]['funds[0].var.covariance_matrix.iloc[2,2]'] / \
    #                                                   raw_data['QE_med_0'][
    #                                                       'funds[0].var.covariance_matrix.iloc[2,2]'] * 100

    rows = []
    for qe, assets in relative_data.items():
        all = {}
        for key_asset, var in assets.items():
            if key_asset in var_list_variance_var_cov:
                for time, val in enumerate(var):
                    if time > 899:
                        all = {}
                        all['QE'] = qe
                        all['asset'] = key_asset
                        all['val'] = val
                        all['time'] = time
                        rows.append(all)
        # all = {}
        # for key_asset, var in assets.items():
        #     if key_asset in var_list_variance_var_cov:
        #         for time, val in enumerate(var):
        #             if time>899:
        #                 all = {}
        #                 all['QE']= qe
        #                 all['asset']=key_asset
        #                 all['val']= val
        #                 all['time']= time
        #                 rows.append(all)

    temp = pd.DataFrame(rows) # all times per experiment
    df_list.append(temp) # all data per seed
df1_cov = pd.concat(df_list, keys=[2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])  # concat seeds


for index, row in df1_cov.iterrows():
    print index
    x = row['QE'].split('_')[2]
    df1_cov.at[index, 'QE'] = x
df1_cov.to_csv('test_cov2.csv') #



def read_pickls_assets(seeds):
    var_list = [
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
    for seed in seeds:
        filename = path + 'raw_and_relative_data_seed_' + str(seed) + '.pkl'
        data = open(filename, "rb")
        list_of_objects = pickle.load(data)
        seedx = list_of_objects[0]
        raw_data = list_of_objects[1]
        relative_data = list_of_objects[2]
        print seed
        # Add a variable for percentage changes in asset holdings


        for key, value in raw_data.items():
            for k2, v2 in value.items():
                value[k2] = v2[0]

        for key, value in relative_data.items():
            for k2, v2 in value.items():
                value[k2] = v2[0]

        for key, value in relative_data.items():
            # assets for funds
            for va in var_list:
                relative_data[key]['percentage_assets'+va] = \
                    relative_data[key][va] / raw_data['QE_med_0'][va] * 100


        temp = pd.DataFrame(data=relative_data)

        df_list.append(temp)

    df1_assets = pd.concat(df_list, keys=[1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])  # use seeds!

    df1_assets.to_csv('test_assets2.csv')

###############################################################################################
###############################################################################################

def read_pickls_timeseries_list(seeds):
    df = pd.DataFrame()
    df_list = []
    for seed in seeds:
        filename = path+ 'raw_and_relative_data_seed_' + str(seed) + '.pkl'
        data = open(filename, "rb")
        list_of_objects = pickle.load(data)
        seedx = list_of_objects[0]
        raw_data = list_of_objects[1]
        relative_data = list_of_objects[2]
        print seed

        for key, value in relative_data.items():
            relative_data[key]['percentage_portfolio2'] = relative_data[key]['portfolios[2].var.price'] / \
                                                          raw_data['QE_med_0'][
                                                              'portfolios[2].var.price'] * 100
            relative_data[key]['percentage_portfolio1'] = relative_data[key]['portfolios[1].var.price'] / \
                                                          raw_data['QE_med_0'][
                                                              'portfolios[1].var.price'] * 100
            relative_data[key]['percentage_portfolio0'] = relative_data[key]['portfolios[0].var.price'] / \
                                                          raw_data['QE_med_0'][
                                                              'portfolios[0].var.price'] * 100
            relative_data[key]['percentage_portfolio3'] = relative_data[key]['portfolios[3].var.price'] / \
                                                          raw_data['QE_med_0'][
                                                              'portfolios[3].var.price'] * 100
        #
        # temp = pd.DataFrame(data=relative_data)
        # df_list.append(temp)
        #
        # df = pd.concat(df_list, keys=[1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        # df.to_csv('cross-sectional-percentage_wide.csv')

        temp = pd.DataFrame(data=relative_data)
        df_list.append(temp)

    df = pd.concat(df_list, keys=[1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    return df


def code_for_percentage_stuff():
    df = pd.DataFrame()
    df_list = []
    for seed in seeds:
        filename = path+ 'raw_and_relative_data_seed_' + str(seed) + '.pkl'
        data = open(filename, "rb")
        list_of_objects = pickle.load(data)
        seedx = list_of_objects[0]
        raw_data = list_of_objects[1]
        relative_data = list_of_objects[2]
        print seed
        for key, value in relative_data.items():
            relative_data[key]['percentage_portfolio2'] = relative_data[key]['portfolios[2].var.price'] / \
                                                          raw_data['QE_med_0'][
                                                              'portfolios[2].var.price'] * 100
            relative_data[key]['percentage_portfolio1'] = relative_data[key]['portfolios[1].var.price'] / \
                                                          raw_data['QE_med_0'][
                                                              'portfolios[1].var.price'] * 100
            relative_data[key]['percentage_portfolio0'] = relative_data[key]['portfolios[0].var.price'] / \
                                                          raw_data['QE_med_0'][
                                                              'portfolios[0].var.price'] * 100
            relative_data[key]['percentage_portfolio3'] = relative_data[key]['portfolios[3].var.price'] / \
                                                          raw_data['QE_med_0'][
                                                              'portfolios[3].var.price'] * 100

            relative_data[key]['percentage_fx_rates.iloc[0,1]'] = relative_data[key]['environment.var.fx_rates.iloc[0,1]'] / \
                                                          raw_data['QE_med_0'][
                                                              'environment.var.fx_rates.iloc[0,1]'] * 100


        temp = pd.DataFrame(data=relative_data)
        df_list.append(temp)


def reshape(df):

    df = (df.set_index(['seed', 'variable'])
       .rename_axis(['QE-Exp'], axis=1)
       .stack()
       .unstack('variable')
       .reset_index())

    l = [i for i in df.columns]

    for i in l:

        for index, row in df.iterrows():
            if 'QE' in i:
                x = row['QE-Exp'].split('_')[2]
                df.at[index, 'QE'] = x
            if 'eff' in i:
                x = row['QE-Exp'].split('_')[2]
                df.at[index, 'QE'] = x

    return df

#df = read_pickls_cross_sectional(seeds)
# read_pickls_assets(seeds)
#
# df1 = pd.read_csv('test_assets2.csv')
# df2=reshape(df1)
# df2.to_csv('assets_long2.csv')










def read_pickls_cross_sectional(seeds):
    df = pd.DataFrame()
    df_list = []
    for seed in seeds:
        filename = path+ 'raw_and_relative_data_seed_' + str(seed) + '.pkl'
        data = open(filename, "rb")
        list_of_objects = pickle.load(data)
        seedx = list_of_objects[0]
        raw_data = list_of_objects[1]
        relative_data = list_of_objects[2]
        print seed
    #

        # Add a variable for percentage changes in asset holdings
        for key, value in relative_data.items():
            # assets for funds[0]

            relative_data[key]['percentage_portfolio3'] = relative_data[key]['portfolios[3].var.price'] / \
                                                          raw_data['QE_med_0'][
                                                              'portfolios[3].var.price'] * 100


        #only take last datapoint
        for key, value in raw_data.items():
            for k2, v2 in value.items():
                value[k2] = v2[0]

        for key, value in relative_data.items():
            for k2, v2 in value.items():
                value[k2] = v2[0]

        temp = pd.DataFrame(data=relative_data)
        df_list.append(temp)

    df1_assets = pd.concat(df_list, keys=[1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])  # use seeds!

    df1_assets.to_csv('test.csv')
    #
    # #
    # for index, row in df1_cov.iterrows():
    #     print index
    #     x = row['qe'].split('_')[2]
    #     df1_cov.at[index, 'qe'] = x
