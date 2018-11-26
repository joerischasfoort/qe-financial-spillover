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

fa0= []
fa1= []
fa2= []
fa3= []

fc0= []
fc1= []

dwa0 = []
dwa1 = []
dwa2 = []
dwa3 = []



dr0 = []
dr1 = []
dr2 = []
dr3 = []

dwc1 = []
dwc0 = []

fwa0 = []
fwa1 = []
fwa2 = []
fwa3 = []

fwc1 = []
fwc0 = []

cov = []
cov_00 = []
cov_11 = []
cov_22 = []
cov_33 = []
cov_01 = []

fx = []
fx_anchor = []
ewma_fx =[]
tau = []



r0 = []
r1 = []
r2 = []
r3 = []

p0 = []
p1 = []
p2 = []
p3 = []

rc0 = []
rc1 = []

red0= []
red1= []

test = []


path = "data/Objects/"
#path = "Experiments/Risk_Aversion/Objects_RA/"

for day in range(1 , 1000):
    filename = path + "objects_day_" + str(day) + "_seed_1"  + "_QE_200"+".pkl"
    #filename = "Experiments/QE/Objects_QE/objects_day_" + str(day) + "_seed_1"  + "_QE_asset_target_0"+".pkl"

    #filename = "C:\Users\jrr\Documents\GitHub\qe-financial-spillover\Experiments\QE\Objects_QE1\objects_day_" + str(day) + "_seed_1"  + "_QE_asset_target_1000"+".pkl"
    data = open(filename,"rb")
    list_of_objects = pickle.load(data)

    portfolios = list_of_objects[0]
    currencies = list_of_objects[1]
    environment = list_of_objects[2]
    exogeneous_agents = list_of_objects[3]
    funds = list_of_objects[4]

    test.append(portfolios[2].par.change_intensity)

    tau.append(environment.var.tau)

    domestic_weight_in_foreign_assets.append(funds[0].var.weights[portfolios[2]]+funds[0].var.weights[portfolios[3]]+funds[0].var.weights[currencies[1]])
    foreign_weight_in_domestic_assets.append(funds[1].var.weights[portfolios[0]]+funds[1].var.weights[portfolios[1]]+funds[1].var.weights[currencies[0]])

    #domestic_weight_in_foreign_assets.append(funds[0].var.weights[portfolios[2]]+funds[0].var.weights[portfolios[3]]+funds[0].var.weights[currencies[1]])
    #foreign_weight_in_domestic_assets.append(funds[1].var.weights[portfolios[0]]+funds[1].var.weights[portfolios[1]]+funds[1].var.weights[currencies[0]])

    dwa0.append(funds[0].var.weights[portfolios[0]])
    dwa1.append(funds[0].var.weights[portfolios[1]])
    dwa2.append(funds[0].var.weights[portfolios[2]])
    dwa3.append(funds[0].var.weights[portfolios[3]])

    dr0.append(funds[0].exp.default_rates[portfolios[0]])
    dr1.append(funds[0].exp.default_rates[portfolios[1]])
    dr2.append(funds[0].exp.default_rates[portfolios[2]])
    dr3.append(funds[0].exp.default_rates[portfolios[3]])







    dwc1.append(funds[0].var.weights[currencies[0]])
    dwc0.append(funds[0].var.weights[currencies[1]])

    da0.append(funds[0].var.assets[portfolios[0]])
    da1.append(funds[0].var.assets[portfolios[1]])
    da2.append(funds[0].var.assets[portfolios[2]])
    da3.append(funds[0].var.assets[portfolios[3]])

    dc0.append(funds[0].var.currency[currencies[0]])
    dc1.append(funds[0].var.currency[currencies[1]])

    fa0.append(funds[1].var.assets[portfolios[0]])
    fa1.append(funds[1].var.assets[portfolios[1]])
    fa2.append(funds[1].var.assets[portfolios[2]])
    fa3.append(funds[1].var.assets[portfolios[3]])

    fc0.append(funds[1].var.currency[currencies[0]])
    fc1.append(funds[1].var.currency[currencies[1]])

    fwa0.append(funds[1].var.weights[portfolios[0]])
    fwa1.append(funds[1].var.weights[portfolios[1]])
    fwa2.append(funds[1].var.weights[portfolios[2]])
    fwa3.append(funds[1].var.weights[portfolios[3]])

    fwc1.append(funds[1].var.weights[currencies[0]])
    fwc0.append(funds[1].var.weights[currencies[1]])

    cov_00.append(funds[0].var.covariance_matrix.loc[portfolios[0], portfolios[0]])
    cov_11.append(funds[0].var.covariance_matrix.loc[portfolios[1], portfolios[1]])
    cov_22.append(funds[0].var.covariance_matrix.loc[portfolios[2], portfolios[2]])
    cov_33.append(funds[0].var.covariance_matrix.loc[portfolios[3], portfolios[3]])
    cov_01.append(funds[0].var.covariance_matrix.loc[portfolios[0], portfolios[1]])


    fx.append(environment.var.fx_rates.iloc[0,1])
    fx_anchor.append(funds[0].exp.exchange_rate_anchor.iloc[0,1])

    ewma_fx.append(1/environment.var.ewma_fx_rates.iloc[0,1])


    r0.append(funds[0].exp.returns[portfolios[0]])
    r1.append(funds[0].exp.returns[portfolios[1]])
    r2.append(funds[0].exp.returns[portfolios[2]])
    r3.append(funds[0].exp.returns[portfolios[3]])


    p0.append(portfolios[0].var.price)
    p1.append(portfolios[1].var.price)
    p2.append(portfolios[2].var.price)
    p3.append(portfolios[3].var.price)


    rc1.append(funds[1].exp.returns[currencies[1]])
    rc0.append(funds[1].exp.returns[currencies[0]])






    red0.append(funds[0].var.redeemable_shares)
    red1.append(funds[1].var.redeemable_shares)


   # p0_pfx.append(portfolios[0].var.price_pfx)
    #p1_pfx.append(portfolios[1].var.price_pfx)


