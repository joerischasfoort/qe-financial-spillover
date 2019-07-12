
import  pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


sys.path.append('/scratch/kzltin001/qe-financial-spillover')
local_dir = "/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_t0_2600/"


var_list_price = [ 'percentage_portfolio2', 'percentage_portfolio1',
                   'percentage_portfolio0' ,'percentage_fx_rates.iloc[0,1]', 'percentage_portfolio3' ]


#20seeds
seeds = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
#5 and 7 did not work
seeds = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 , 23, 24]

'''
Remember that I multiply by 100!!!!!!!!!!!!!!
'''
df = pd.DataFrame()
df_list = []


var_list_risk_fund_0 = \
              [
            'funds[0].exp.returns[portfolios[0]]',   # domestic bond - leave to test later
            "funds[0].var.covariance_matrix.iloc[0,0]" , # domestic bond
            "funds[0].var.covariance_matrix.iloc[1,1]" , # domestic equity
            "funds[0].var.covariance_matrix.iloc[2,2]" , #  foreign bond
            "funds[0].var.covariance_matrix.iloc[3,3]" , # foreign equity
            'percentage_fund0_var1',
            'percentage_fund0_var2',
            'percentage_fund0_var0',
            'percentage_fund0_var3',

            ############## COVARS

            "funds[0].var.covariance_matrix.iloc[0,1]" , # domestic bond  vs domestic equity
            "funds[0].var.covariance_matrix.iloc[0,2]" , # domestic bond vs  foreign bond  
            "funds[0].var.covariance_matrix.iloc[0,3]" , #  domestic bond   vs  foreign equity
            "funds[0].var.covariance_matrix.iloc[2,3]" , # foreign bond vs foreign equity
            "funds[0].var.covariance_matrix.iloc[1,3]" , # domestic equity vs foreign equity
            'percentage_fund0_covar01',
            'percentage_fund0_covar02',
            'percentage_fund0_covar03',
            'percentage_fund0_covar23',
            'percentage_fund0_covar13',

              ]

var_list_risk_fund_2 = \
              [
            'funds[2].exp.returns[portfolios[0]]',   # domestic bond - leave to test later
            "funds[2].var.covariance_matrix.iloc[0,0]" , # domestic bond
            "funds[2].var.covariance_matrix.iloc[1,1]" , # domestic equity
            "funds[2].var.covariance_matrix.iloc[2,2]" , #  foreign bond
            "funds[2].var.covariance_matrix.iloc[3,3]" , # foreign equity
            'percentage_fund2_var1',
            'percentage_fund2_var2',
            'percentage_fund2_var0',
            'percentage_fund2_var3',


            ############## COVARS

            "funds[2].var.covariance_matrix.iloc[0,1]" , # domestic bond  vs domestic equity
            "funds[2].var.covariance_matrix.iloc[0,2]" , # domestic bond vs  foreign bond  
            "funds[2].var.covariance_matrix.iloc[0,3]" , #  domestic bond   vs  foreign equity
            "funds[2].var.covariance_matrix.iloc[2,3]" , # foreign bond vs foreign equity
            "funds[2].var.covariance_matrix.iloc[1,3]" , # domestic equity vs foreign equity
            'percentage_fund2_covar01',
            'percentage_fund2_covar02',
            'percentage_fund2_covar03',
            'percentage_fund2_covar23',
            'percentage_fund2_covar13',
              ]

var_list_risk_fund_3 = \
              [
            'funds[3].exp.returns[portfolios[0]]',   # domestic bond - leave to test later
            "funds[3].var.covariance_matrix.iloc[0,0]" , # domestic bond
            "funds[3].var.covariance_matrix.iloc[1,1]" , # domestic equity
            "funds[3].var.covariance_matrix.iloc[2,2]" , #  foreign bond
            "funds[3].var.covariance_matrix.iloc[3,3]" , # foreign equity
            'percentage_fund3_var1',
            'percentage_fund3_var2',
            'percentage_fund3_var0',
            'percentage_fund3_var3'



            ############## COVARS

            "funds[3].var.covariance_matrix.iloc[0,1]" , # domestic bond  vs domestic equity
            "funds[3].var.covariance_matrix.iloc[0,2]" , # domestic bond vs  foreign bond  
            "funds[3].var.covariance_matrix.iloc[0,3]" , #  domestic bond   vs  foreign equity
            "funds[3].var.covariance_matrix.iloc[2,3]" , # foreign bond vs foreign equity
            "funds[3].var.covariance_matrix.iloc[1,3]" , # domestic equity vs foreign equity
            'percentage_fund3_covar01',
            'percentage_fund3_covar02',
            'percentage_fund3_covar03',
            'percentage_fund3_covar23',
            'percentage_fund3_covar13',

              ]

##########################
############# START
##########################

print('############# Reading risk.. FUND 0########')
for seed in seeds:
    filename = local_dir + '2600_Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'
    data = open(filename, "rb")
    list_of_objects = pickle.load(data)
    seedx = list_of_objects[0]
    raw_data = list_of_objects[1]
    relative_data = list_of_objects[2]
    print seed, 'CREATE RISK percentage data'

    for key, value in relative_data.items():
        relative_data[key]['percentage_fund0_covar01'] = relative_data[key]['funds[0].var.covariance_matrix.iloc[0,1]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[0].var.covariance_matrix.iloc[0,1]'] * 100
        relative_data[key]['percentage_fund0_covar02'] = relative_data[key]['funds[0].var.covariance_matrix.iloc[0,2]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[0].var.covariance_matrix.iloc[0,2]'] * 100


        relative_data[key]['percentage_fund0_covar03'] = relative_data[key]['funds[0].var.covariance_matrix.iloc[0,3]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[0].var.covariance_matrix.iloc[0,3]'] * 100

        relative_data[key]['percentage_fund0_covar23'] = relative_data[key]['funds[0].var.covariance_matrix.iloc[2,3]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[0].var.covariance_matrix.iloc[2,3]'] * 100


        relative_data[key]['percentage_fund0_covar13'] = relative_data[key]['funds[0].var.covariance_matrix.iloc[1,3]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[0].var.covariance_matrix.iloc[1,3]'] * 100


                                                        

        relative_data[key]['percentage_fund0_var0'] = relative_data[key]['funds[0].var.covariance_matrix.iloc[0,0]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[0].var.covariance_matrix.iloc[0,0]'] * 100
        relative_data[key]['percentage_fund0_var1'] = relative_data[key]['funds[0].var.covariance_matrix.iloc[1,1]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[0].var.covariance_matrix.iloc[1,1]'] * 100
        relative_data[key]['percentage_fund0_var2'] = relative_data[key]['funds[0].var.covariance_matrix.iloc[2,2]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[0].var.covariance_matrix.iloc[2,2]'] * 100

        relative_data[key]['percentage_fund0_var3'] = relative_data[key]['funds[0].var.covariance_matrix.iloc[3,3]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[0].var.covariance_matrix.iloc[3,3]'] * 100




    rows = []

    for qe, assets in relative_data.items():
        all = {}
        #
        for key_asset, var in assets.items():
            if key_asset in var_list_risk_fund_0:   ## CAREFUL!

                for time, val in enumerate(var):
                    all = {}
                    all['seed'] = seed

                    list_temp = []
                    list_temp.append(qe)

                    #print list_temp[0][qe.find('_', 10):] This drags out the QE

                    all['QE'] = list_temp[0][qe.find('_', 15) + 5:]
                    all['asset'] = key_asset
                    all['val'] = val
                    all['time'] = time
                    #print time
                    rows.append(all)

    temp = pd.DataFrame(rows) # all times per experiment
    df_list.append(temp) # all data per seed
df_risk_fund_0 = pd.concat(df_list, keys=seeds,  sort=True)  #  ## CAREFUL!


print('############# Reading risk.. FUND 2########')
for seed in seeds:
    filename = local_dir + '2600_Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'
    data = open(filename, "rb")
    list_of_objects = pickle.load(data)
    seedx = list_of_objects[0]
    raw_data = list_of_objects[1]
    relative_data = list_of_objects[2]
    print seed, 'CREATE RISK percentage data'

    for key, value in relative_data.items():
        relative_data[key]['percentage_fund2_var0'] = relative_data[key]['funds[2].var.covariance_matrix.iloc[0,0]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[2].var.covariance_matrix.iloc[0,0]'] * 100
        relative_data[key]['percentage_fund2_var1'] = relative_data[key]['funds[2].var.covariance_matrix.iloc[1,1]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[2].var.covariance_matrix.iloc[1,1]'] * 100
        relative_data[key]['percentage_fund2_var2'] = relative_data[key]['funds[2].var.covariance_matrix.iloc[2,2]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[2].var.covariance_matrix.iloc[2,2]'] * 100

        relative_data[key]['percentage_fund2_var3'] = relative_data[key]['funds[2].var.covariance_matrix.iloc[3,3]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[2].var.covariance_matrix.iloc[3,3]'] * 100



        relative_data[key]['percentage_fund2_covar01'] = relative_data[key]['funds[2].var.covariance_matrix.iloc[0,1]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[2].var.covariance_matrix.iloc[0,1]'] * 100
        relative_data[key]['percentage_fund2_covar02'] = relative_data[key]['funds[2].var.covariance_matrix.iloc[0,2]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[2].var.covariance_matrix.iloc[0,2]'] * 100


        relative_data[key]['percentage_fund2_covar03'] = relative_data[key]['funds[2].var.covariance_matrix.iloc[0,3]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[2].var.covariance_matrix.iloc[0,3]'] * 100

        relative_data[key]['percentage_fund2_covar23'] = relative_data[key]['funds[2].var.covariance_matrix.iloc[2,3]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[2].var.covariance_matrix.iloc[2,3]'] * 100


        relative_data[key]['percentage_fund2_covar13'] = relative_data[key]['funds[2].var.covariance_matrix.iloc[1,3]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[2].var.covariance_matrix.iloc[1,3]'] * 100


                                                    
    rows = []

    for qe, assets in relative_data.items():
        all = {}
        #
        for key_asset, var in assets.items():
            if key_asset in var_list_risk_fund_2:   ## CAREFUL!

                for time, val in enumerate(var):
                    all = {}
                    all['seed'] = seed

                    list_temp = []
                    list_temp.append(qe)

                    #print list_temp[0][qe.find('_', 10):] This drags out the QE

                    all['QE'] = list_temp[0][qe.find('_', 15) + 5:]
                    all['asset'] = key_asset
                    all['val'] = val
                    all['time'] = time
                    #print time
                    rows.append(all)

    temp = pd.DataFrame(rows) # all times per experiment
    df_list.append(temp) # all data per seed
df_risk_fund_2 = pd.concat(df_list, keys=seeds,  sort=True)  #  ## CAREFUL!

print('############# Reading risk.. FUND 3########')
for seed in seeds:
    filename = local_dir + '2600_Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'
    data = open(filename, "rb")
    list_of_objects = pickle.load(data)
    seedx = list_of_objects[0]
    raw_data = list_of_objects[1]
    relative_data = list_of_objects[2]
    print seed, 'CREATE RISK percentage data'

    for key, value in relative_data.items():
        relative_data[key]['percentage_fund3_var0'] = relative_data[key]['funds[3].var.covariance_matrix.iloc[0,0]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[3].var.covariance_matrix.iloc[0,0]'] * 100
        relative_data[key]['percentage_fund3_var1'] = relative_data[key]['funds[3].var.covariance_matrix.iloc[1,1]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[3].var.covariance_matrix.iloc[1,1]'] * 100
        relative_data[key]['percentage_fund3_var2'] = relative_data[key]['funds[3].var.covariance_matrix.iloc[2,2]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[3].var.covariance_matrix.iloc[2,2]'] * 100

        relative_data[key]['percentage_fund3_var3'] = relative_data[key]['funds[3].var.covariance_matrix.iloc[3,3]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[3].var.covariance_matrix.iloc[3,3]'] * 100



        relative_data[key]['percentage_fund3_covar01'] = relative_data[key]['funds[3].var.covariance_matrix.iloc[0,1]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[3].var.covariance_matrix.iloc[0,1]'] * 100
        relative_data[key]['percentage_fund3_covar02'] = relative_data[key]['funds[3].var.covariance_matrix.iloc[0,2]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[3].var.covariance_matrix.iloc[0,2]'] * 100


        relative_data[key]['percentage_fund3_covar03'] = relative_data[key]['funds[3].var.covariance_matrix.iloc[0,3]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[3].var.covariance_matrix.iloc[0,3]'] * 100

        relative_data[key]['percentage_fund3_covar23'] = relative_data[key]['funds[3].var.covariance_matrix.iloc[2,3]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[3].var.covariance_matrix.iloc[2,3]'] * 100


        relative_data[key]['percentage_fund3_covar13'] = relative_data[key]['funds[3].var.covariance_matrix.iloc[1,3]'] / \
                                                      raw_data['_seed_' +str(seed)  + '_Long_SIM_med_QE0'][
                                                          'funds[3].var.covariance_matrix.iloc[1,3]'] * 100


                                                                                                               

    rows = []

    for qe, assets in relative_data.items():
        all = {}
        #
        for key_asset, var in assets.items():
            if key_asset in var_list_risk_fund_3:   ## CAREFUL!

                for time, val in enumerate(var):
                    all = {}
                    all['seed'] = seed

                    list_temp = []
                    list_temp.append(qe)

                    #print list_temp[0][qe.find('_', 10):] This drags out the QE

                    all['QE'] = list_temp[0][qe.find('_', 15) + 5:]
                    all['asset'] = key_asset
                    all['val'] = val
                    all['time'] = time
                    #print time
                    rows.append(all)

    temp = pd.DataFrame(rows) # all times per experiment
    df_list.append(temp) # all data per seed
df_risk_fund_3 = pd.concat(df_list, keys=seeds,  sort=True)   ## CAREFUL with name of df


 
#Saving  
# df_assets.to_csv('df_assets.csv') 
# df_prices.to_csv('df_prices.csv')
# df_exp_returns.to_csv('df_exp_returns.csv')
# df_assets.to_pickle('df_assets.pickle')
# df_prices.to_pickle('df_prices.pickle')
# df_exp_returns.to_pickle('df_exp_returns.pickle')
# df_prices= pd.read_pickle(local_dir+'df_prices.pickle')
# df_exp_returns = pd.read_pickle(local_dir+'df_exp_returns.pickle')

df_list = [ df_risk_fund_0, df_risk_fund_2, df_risk_fund_3 ] 
df_final = pd.concat(df_list, keys=['risk_fund_0', 'risk_fund_2', 'risk_fund_3'])  # concat seeds


df_final = df_final.iloc[:, 0:]
df_varcovar = df_final.pivot_table(columns=['asset'], index=['QE', 'seed', 'time'], values='val')

df_varcovar.to_csv('df_varcovar.csv')
# df_list = [ df_prices, df_exp_returns ] 

# df_final = pd.concat(df_list, keys=['prices', 'returns'])  # concat seeds
# df_final = df_final.iloc[:, 3:]
# df_final = df_final.pivot_table(columns=['asset'], index=['QE', 'seed', 'time'], values='val')

