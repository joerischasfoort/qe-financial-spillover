import  pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from spillover_model_calRA import *
from spillover_model import *
from calibration_functions import *##variables to extract
import pandas as pd


domestic_weight_in_foreign_assets=[]
foreign_weight_in_domestic_assets=[]

seed = 1
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



dr00 = []
dr01 = []
dr02 = []
dr03 = []
dr04 = []
dr05 = []


dr10 = []
dr11 = []
dr12 = []
dr13 = []
dr14 = []
dr15 = []

dr20 = []
dr21 = []
dr22 = []
dr23 = []
dr24 = []
dr25 = []

dr30 = []
dr31 = []
dr32 = []
dr33 = []
dr34 = []
dr35 = []


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


path = "C:/Users/jrr/Dropbox/GitHub/qe-financial-spillover/data/Objects_final/"
#path = "Experiments/Risk_Aversion/Objects_RA/"

for day in range(300 , 501):
    filename = path + "objects_day_102_seed_1_4aSim_Cal_"+ str(day)+".pkl"
    #filename = path + "objects_day_1_seed_1_4aSim_intRA_"+ str(day)+".pkl"

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

    dr00.append(funds[0].par.RA_matrix.loc[portfolios[0]][portfolios[0]])
    dr01.append(funds[0].par.RA_matrix.loc[portfolios[1]][portfolios[1]])
    dr02.append(funds[0].par.RA_matrix.loc[portfolios[2]][portfolios[2]])
    dr03.append(funds[0].par.RA_matrix.loc[portfolios[3]][portfolios[3]])
    dr04.append(funds[0].par.RA_matrix.loc[currencies[0]][currencies[0]])
    dr05.append(funds[0].par.RA_matrix.loc[currencies[1]][currencies[1]])

    dr10.append(funds[1].par.RA_matrix.loc[portfolios[0]][portfolios[0]])
    dr11.append(funds[1].par.RA_matrix.loc[portfolios[1]][portfolios[1]])
    dr12.append(funds[1].par.RA_matrix.loc[portfolios[2]][portfolios[2]])
    dr13.append(funds[1].par.RA_matrix.loc[portfolios[3]][portfolios[3]])
    dr14.append(funds[1].par.RA_matrix.loc[currencies[0]][currencies[0]])
    dr15.append(funds[1].par.RA_matrix.loc[currencies[1]][currencies[1]])

    dr20.append(funds[2].par.RA_matrix.loc[portfolios[0]][portfolios[0]])
    dr21.append(funds[2].par.RA_matrix.loc[portfolios[1]][portfolios[1]])
    dr22.append(funds[2].par.RA_matrix.loc[portfolios[2]][portfolios[2]])
    dr23.append(funds[2].par.RA_matrix.loc[portfolios[3]][portfolios[3]])
    dr24.append(funds[2].par.RA_matrix.loc[currencies[0]][currencies[0]])
    dr25.append(funds[2].par.RA_matrix.loc[currencies[1]][currencies[1]])

    dr30.append(funds[3].par.RA_matrix.loc[portfolios[0]][portfolios[0]])
    dr31.append(funds[3].par.RA_matrix.loc[portfolios[1]][portfolios[1]])
    dr32.append(funds[3].par.RA_matrix.loc[portfolios[2]][portfolios[2]])
    dr33.append(funds[3].par.RA_matrix.loc[portfolios[3]][portfolios[3]])
    dr34.append(funds[3].par.RA_matrix.loc[currencies[0]][currencies[0]])
    dr35.append(funds[3].par.RA_matrix.loc[currencies[1]][currencies[1]])

    dwc0.append(funds[1].var.weights[currencies[0]])
    dwc1.append(funds[1].var.weights[currencies[1]])

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
    cov_01.append(funds[0].var.covariance_matrix.loc[portfolios[0], portfolios[2]])


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


mean_RA =[{'agent':str(0),'asset0': np.mean(dr00),'asset1': np.mean(dr01),'asset2': np.mean(dr02),'asset3': np.mean(dr03),'currency0': np.mean(dr04),'currency1': np.mean(dr05)}, {'agent':str(1),'asset0':np.mean(dr10),'asset1':np.mean(dr11),'asset2':np.mean(dr12),'asset3':np.mean(dr13),'currency0':np.mean(dr14),'currency1':np.mean(dr15)}, {'agent':str(2),'asset0':np.mean(dr20),'asset1':np.mean(dr21),'asset2':np.mean(dr22),'asset3':np.mean(dr23),'currency0':np.mean(dr24),'currency1':np.mean(dr25)},{'agent':str(3),'asset0':np.mean(dr30),'asset1':np.mean(dr31),'asset2':np.mean(dr32),'asset3':np.mean(dr33),'currency0':np.mean(dr34),'currency1':np.mean(dr35)}]
mean_RA = pd.DataFrame(mean_RA)

std_RA =[{'agent':str(0),'asset0': np.std(dr00)/np.mean(dr00),'asset1': np.std(dr01)/np.mean(dr01),'asset2': np.std(dr02)/np.mean(dr02),'asset3': np.std(dr03)/np.mean(dr03),'currency0': np.std(dr04)/ np.mean(dr04),'currency1': np.std(dr05)/np.mean(dr05)}, {'agent':str(1),'asset0':np.std(dr10)/np.mean(dr10),'asset1':np.std(dr11)/np.mean(dr11),'asset2':np.std(dr12)/np.mean(dr12),'asset3':np.std(dr13)/np.mean(dr13),'currency0':np.std(dr14)/ np.mean(dr14),'currency1':np.std(dr15)/np.mean(dr15)}, {'agent':str(2),'asset0':np.std(dr20)/np.mean(dr20),'asset1':np.std(dr21)/np.mean(dr21),'asset2':np.std(dr22)/np.mean(dr22),'asset3':np.std(dr23)/np.mean(dr23),'currency0':np.std(dr24)/ np.mean(dr24),'currency1':np.std(dr25)/np.mean(dr25)},{'agent':str(3),'asset0':np.std(dr30)/np.mean(dr30),'asset1':np.std(dr31)/np.mean(dr31),'asset2':np.std(dr32)/np.mean(dr32),'asset3':np.std(dr33)/np.mean(dr33),'currency0':np.std(dr34)/ np.mean(dr34),'currency1':np.std(dr35)/np.mean(dr35)}]
std_RA = pd.DataFrame(std_RA)


writer = pd.ExcelWriter('Calibrated_RAs.xlsx')
mean_RA.to_excel(writer, 'Sheet1')
std_RA.to_excel(writer, 'Sheet2')
writer.save()

#
    #
#path = "C:/Users/jrr/Dropbox/GitHub/qe-financial-spillover/data/Objects/"
#
#saving_params = {}
#saving_params.update({"path": 'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects'})
#
#filename = path + "objects_day_5101_seed_1_4aSim_CalRA_9.pkl"
##filename = "Experiments/QE/Objects_QE/objects_day_" + str(day) + "_seed_1"  + "_QE_asset_target_0"+".pkl"
#
##filename = "C:\Users\jrr\Documents\GitHub\qe-financial-spillover\Experiments\QE\Objects_QE1\objects_day_" + str(day) + "_seed_1"  + "_QE_asset_target_1000"+".pkl"
#data = open(filename,"rb")
#list_of_objects = pickle.load(data)
#
#portfolios_cal = list_of_objects[0]
#currencies_cal = list_of_objects[1]
#environment_cal = list_of_objects[2]
#exogenous_agents_cal = list_of_objects[3]
#funds_cal = list_of_objects[4]
#
#portfolios_init, currencies_init, funds_init, environment_init, exogenous_agents_init = init_port_holdings_4f(seed)
#
#
## set prices to 1
#portfolios_cal = approach_prices(portfolios_cal, approach_speed=1)
#for a in portfolios_cal:
#    a.var_previous.price = a.var.price
#
#for f in funds_cal:
#    s = recompute_liabilities(f, portfolios_cal, currencies_cal, environment_cal)
#    f.var_previous.redeemable_shares = s
#
#var = copy.copy(portfolios_cal)
#var.append("FX")
#obj_label = "test"
#environment_cal.par.global_parameters["start_day"] = 5001
#environment_cal.par.global_parameters["end_day"] = environment_cal.par.global_parameters["start_day"] + 1
#environment_cal.par.global_parameters['cov_memory'] = 0
#environment_cal.par.global_parameters['conv_bound'] = 0.001
#saving_params.update({"time": environment_cal.par.global_parameters["end_day"] - 1})
#portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t = spillover_model_calRA(
#    portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, seed, obj_label, saving_params,
#    var)
#
#funds_cal, portfolios_cal = approach_balance_sheets(funds_cal, portfolios_cal, currencies_cal, environment_cal,
#                                                    funds_init,
#                                                    portfolios_init, currencies_init, cur_dummy=0)
#
## update redeemable shares and interest rates
#var = [str(f) + "_" + str(a) for f in funds_cal for a in portfolios_cal]
#for a in portfolios_cal:
#    var.append(a)
#var.append("FX")
#environment_cal.par.global_parameters["start_day"] = 5001
#environment_cal.par.global_parameters["end_day"] = environment_cal.par.global_parameters["start_day"] + 1
#environment_cal.par.global_parameters['cov_memory'] = 0
#environment_cal.par.global_parameters['conv_bound'] = 0.01
#saving_params.update({"time": environment_cal.par.global_parameters["end_day"] - 1})
#
#portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, data_t = spillover_model_calRA(
#    portfolios_cal,
#    currencies_cal,
#    environment_cal,
#    exogenous_agents_cal,
#    funds_cal, seed,
#    obj_label,
#    saving_params, var)
#