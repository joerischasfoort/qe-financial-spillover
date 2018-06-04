import  pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

assets_target = [0, 100, 500, 2500]
for i in assets_target:
    obj_label = "QE_asset_target_" + str(i)


    #variables to extract
    DW_in_FA=[]
    FW_in_DA=[]
    cov_00 = []
    cov_11 = []
    fx = []
    p1 = []
    p0 = []
    r0 = []
    r1 = []


    for day in range(10000,10010):
        filename = "data/Objects_QE/objects_day_" + str(day) + "_seed_1_"  + obj_label+".pkl"
        data = open(filename,"rb")
        list_of_objects = pickle.load(data)

        portfolios = list_of_objects[0]
        currencies = list_of_objects[1]
        environment = list_of_objects[2]
        exogeneous_agents = list_of_objects[3]
        funds = list_of_objects[4]


        DW_in_FA.append(funds[0].var.weights[portfolios[1]]+funds[0].var.weights[currencies[1]])
        FW_in_DA.append(funds[1].var.weights[portfolios[0]]+funds[1].var.weights[currencies[0]])

        cov_11.append(funds[1].var.covariance_matrix.loc[portfolios[1],portfolios[1]])
        cov_00.append(funds[1].var.covariance_matrix.loc[portfolios[0], portfolios[0]])

        fx.append(1/environment.var.fx_rates.iloc[0,1])

        p1.append(portfolios[1].var.price)
        p0.append(portfolios[0].var.price)
        r1.append(funds[1].exp.returns[portfolios[1]])
        r0.append(funds[1].exp.returns[portfolios[0]])

    exec("DW_in_FA" +"_"+ obj_label +"= DW_in_FA")
    exec ("FW_in_DA" +"_"+ obj_label +"= FW_in_DA")
    exec("cov_00" +"_"+ obj_label +"= cov_00")
    exec ("cov_11" +"_"+ obj_label +"= cov_11")
    exec("fx" +"_"+ obj_label +"= fx")
    exec ("p0" +"_"+ obj_label +"= p0")
    exec("p1" +"_"+ obj_label +"= p1")
    exec ("r0" +"_"+ obj_label +"= r0")
    exec ("r1" + "_" + obj_label +"= r1")


