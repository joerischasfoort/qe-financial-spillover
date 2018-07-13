import  pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#variables to extract
domestic_weight_in_foreign_assets=[]
foreign_weight_in_domestic_assets=[]

da0= []
da1= []
da2= []
da3= []
dc0= []
dc1= []

cov = []
cov_00 = []
cov_11 = []
cov_01 = []
fx = []
ewma_fx =[]
tau = []
p1 = []
p0 = []
p2 = []
p3 = []
r0 = []
r1 = []
rc0 = []
rc1 = []
r2 = []
r3 = []

red0= []
red1= []

p0_pfx = []
p1_pfx = []

for day in range(4501,4600):
    filename = "data/Objects/objects_day_" + str(day) + "_seed_1"  + "_x"+".pkl"
    filename = "data/Objects/objects_day_" + str(day) + "_seed_1"  + "_QE_asset_target_1000"+".pkl"

    #filename = "C:\Users\jrr\Documents\GitHub\qe-financial-spillover\Experiments\QE\Objects_QE1\objects_day_" + str(day) + "_seed_1"  + "_QE_asset_target_1000"+".pkl"
    data = open(filename,"rb")
    list_of_objects = pickle.load(data)

    portfolios = list_of_objects[0]
    currencies = list_of_objects[1]
    environment = list_of_objects[2]
    exogeneous_agents = list_of_objects[3]
    funds = list_of_objects[4]

    tau.append(environment.var.tau)

    domestic_weight_in_foreign_assets.append(funds[0].var.weights[portfolios[1]]+funds[0].var.weights[currencies[1]])
    foreign_weight_in_domestic_assets.append(funds[1].var.weights[portfolios[0]]+funds[1].var.weights[currencies[0]])

    #domestic_weight_in_foreign_assets.append(funds[0].var.weights[portfolios[2]]+funds[0].var.weights[portfolios[3]]+funds[0].var.weights[currencies[1]])
    #foreign_weight_in_domestic_assets.append(funds[1].var.weights[portfolios[0]]+funds[1].var.weights[portfolios[1]]+funds[1].var.weights[currencies[0]])


    da0.append(funds[0].var.assets[portfolios[0]])
    da1.append(funds[1].var.assets[portfolios[0]])
    da2.append(exogeneous_agents["underwriter"].var.assets[portfolios[0]])
    da3.append(funds[1].var.weights[portfolios[1]])
    dc0.append(funds[0].var.weights[currencies[0]])
    dc1.append(funds[0].var.weights[currencies[1]])

    cov_00.append(funds[0].var.covariance_matrix.loc[currencies[1], currencies[1]])
    cov_11.append(funds[1].var.covariance_matrix.loc[currencies[1], currencies[1]])
    cov_01.append(funds[1].var.covariance_matrix.loc[portfolios[1], portfolios[1]])


    fx.append(environment.var.fx_rates.iloc[0,1])

    ewma_fx.append(1/environment.var.ewma_fx_rates.iloc[0,1])

    p1.append(portfolios[1].var.price)
    p0.append(portfolios[0].var.price)
    r1.append(funds[0].exp.returns[portfolios[1]])
    r0.append(funds[0].exp.returns[portfolios[0]])

    rc1.append(funds[1].exp.returns[currencies[1]])
    rc0.append(funds[1].exp.returns[currencies[0]])

    #p2.append(portfolios[2].var.price)
    #p3.append(portfolios[3].var.price)
    #r2.append(funds[0].exp.returns[portfolios[2]])
    #r3.append(funds[0].exp.returns[portfolios[3]])


    red0.append(funds[0].var.redeemable_shares)
    red1.append(funds[1].var.redeemable_shares)


    p0_pfx.append(portfolios[0].var.price_pfx)
    p1_pfx.append(portfolios[1].var.price_pfx)

