import  pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools
import sys

from extract.asset_holdings import *

################    #################    #################
#################    #################    #################

#Execute selection of code (possible in pycharm, unpickling .pkl in jupyter yields import error)

local_dir = "/Users/Tina/git_repos/qe-financial-spillover/Experiments/Marketsize/Objects_Marketsize/"
#local_dir = "/Volumes/QE/kzltin001/Marketsize/Objects_marketsize/"
# Domestic marketsize variation (domestic market * variable = foreign market size)
variable = [0.05, 0.1, 0.15, 0.2, 0.5 , 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


#read data into dictionaries according to marketsize
fx_dict = {}
p0_dict = {}
p1_dict = {}

d_dc_dict = {}
d_fc_dict = {}
d_da_dict = {}
d_fa_dict = {}

f_dc_dict = {}
f_fc_dict = {}
f_da_dict = {}
f_fa_dict = {}

d_dc_dict_assets = {}
d_fc_dict_assets = {}
d_da_dict_assets = {}
d_fa_dict_assets = {}

f_dc_dict_assets = {}
f_fc_dict_assets = {}
f_da_dict_assets = {}
f_fa_dict_assets = {}


for i in variable:
    obj_label =  "Marketsize_" + str(i)

    #variables to extract
    # Prices
    p0 = []
    p1 = []
    fx = []
    # Domestic representative agent weights
    d_dc = []
    d_fc = []
    d_da = []
    d_fa = []

    # Foreign representative agents weights
    f_dc = []
    f_fc = []
    f_da = []
    f_fa = []

    # Domestic representative agent assets
    d_dc_assets = []
    d_fc_assets = []
    d_da_assets = []
    d_fa_assets = []

    # Foreign representative agents assets
    f_dc_assets = []
    f_fc_assets = []
    f_da_assets = []
    f_fa_assets = []
    ############################
    # After burn-in phase, read data into lists

    for day in range(4000,4999):
        filename = local_dir + "objects_day_" + str(day) + "_seed_1_"  + obj_label+".pkl"
        data = open(filename,"rb")
        list_of_objects = pickle.load(data)

        portfolios = list_of_objects[0]
        currencies = list_of_objects[1]
        environment = list_of_objects[2]
        exogeneous_agents = list_of_objects[3]
        funds = list_of_objects[4]

        # Prices
        fx.append(environment.var.fx_rates.iloc[0,1])
        p0.append(portfolios[0].var.price)
        p1.append(portfolios[1].var.price)

        #Weights
        d_dc.append(funds[0].var.weights[currencies[0]])
        d_fc.append(funds[0].var.weights[currencies[1]])
        d_da.append(funds[0].var.weights[portfolios[0]])
        d_fa.append(funds[0].var.weights[portfolios[1]])

        f_dc.append(funds[1].var.weights[currencies[0]])
        f_fc.append(funds[1].var.weights[currencies[1]])
        f_da.append(funds[1].var.weights[portfolios[0]])
        f_fa.append(funds[1].var.weights[portfolios[1]])

        #assets
        d_dc_assets.append(funds[0].var.currency[currencies[0]])
        d_fc_assets.append(funds[0].var.currency[currencies[1]])
        d_da_assets.append(funds[0].var.assets[portfolios[0]])
        d_fa_assets.append(funds[0].var.assets[portfolios[1]])

        f_dc_assets.append(funds[1].var.currency[currencies[0]])
        f_fc_assets.append(funds[1].var.currency[currencies[1]])
        f_da_assets.append(funds[1].var.assets[portfolios[0]])
        f_fa_assets.append(funds[1].var.assets[portfolios[1]])

        print day

#################    #################    #################
##### Update Dictionaries with lists                 ######
#################    #################    #################


    #Dictionaries
    fx_dict.update({obj_label: fx})
    p0_dict.update({obj_label: p0})
    p1_dict.update({obj_label: p1})

    #Weights
    d_dc_dict.update({obj_label: d_dc})
    d_fc_dict.update({obj_label: d_fc})
    d_da_dict.update({obj_label: d_da})
    d_fa_dict.update({obj_label: d_fa})

    f_dc_dict.update({obj_label: f_dc})
    f_fc_dict.update({obj_label: f_fc})
    f_da_dict.update({obj_label: f_da})
    f_fa_dict.update({obj_label: f_fa})

    # Assets
    d_dc_dict_assets.update({obj_label: d_dc_assets})
    d_fc_dict_assets.update({obj_label: d_fc_assets})
    d_da_dict_assets.update({obj_label: d_da_assets})
    d_fa_dict_assets.update({obj_label: d_fa_assets})

    f_dc_dict_assets.update({obj_label: f_dc_assets})
    f_fc_dict_assets.update({obj_label: f_fc_assets})
    f_da_dict_assets.update({obj_label: f_da_assets})
    f_fa_dict_assets.update({obj_label: f_fa_assets})

##############################
#
##Averaging over time
#
#Create Numpy arrays for moments
##############################
##############################

D_DA_mean, D_DA_5, D_DA_95,\
D_DC_mean, D_DC_5, D_DC_95,\
D_FA_mean, D_FA_5, D_FA_95, \
D_FC_mean, D_FC_5, D_FC_95 = extract_domestic_agent_assets(fx_dict,  d_dc_dict_assets, d_fc_dict_assets , d_da_dict_assets , d_fa_dict_assets)

#
# FX =np.empty((0,2), float)
#
# FX_mean = np.empty((0,2), float)
# FX_5 =np.empty((0,2), float)
# FX_95 =np.empty((0,2), float)
#
#
# # For WEIGHTS

# F_DC_mean = np.empty((0,2), float)
# F_DC_5 =np.empty((0,2), float)
# F_DC_95 =np.empty((0,2), float)
#
# F_FC_mean = np.empty((0,2), float)
# F_FC_5 =np.empty((0,2), float)
# F_FC_95 =np.empty((0,2), float)
#
# F_DA_mean = np.empty((0,2), float)
# F_DA_5 =np.empty((0,2), float)
# F_DA_95 =np.empty((0,2), float)
#
# F_FA_mean = np.empty((0,2), float)
# F_FA_5 =np.empty((0,2), float)
# F_FA_95 =np.empty((0,2), float)
# ##########################################
#
#
#
# for i in sorted(fx_dict.iterkeys()):
#     f=  np.array(fx_dict[i])
#
#     FX=np.append(FX, np.array([[float(i.split("_")[-1]),np.std(f)]]),axis=0)
#     FX_mean=np.append(FX_mean, np.array([[float(i.split("_")[-1]),np.mean(f)]]),axis=0)
#     FX_5 = np.append(FX_5, np.array([[float(i.split("_")[-1]), np.percentile(f, 5)]]), axis=0)
#     FX_95 = np.append(FX_95, np.array([[float(i.split("_")[-1]), np.percentile(f, 95)]]), axis=0)
#
#     D_DC_mean = np.append(D_DC_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_dc_dict[i]))]]), axis=0)
#     D_FC_mean = np.append(D_FC_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_fc_dict[i]))]]), axis=0)
#     D_DA_mean = np.append(D_DA_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_da_dict[i]))]]), axis=0)
#     D_FA_mean = np.append(D_FA_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_fa_dict[i]))]]), axis=0)
#
#     D_DC_5 = np.append(D_DC_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_dc_dict[i]), 5)]]), axis=0)
#     D_FC_5 = np.append(D_FC_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_fc_dict[i]), 5)]]), axis=0)
#     D_DA_5 = np.append(D_DA_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_da_dict[i]), 5)]]), axis=0)
#     D_FA_5 = np.append(D_FA_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_fa_dict[i]), 5)]]), axis=0)
#
#     D_DC_95 = np.append(D_DC_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_dc_dict[i]), 95)]]),axis=0)
#     D_FC_95 = np.append(D_FC_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_fc_dict[i]), 95)]]),axis=0)
#     D_DA_95 = np.append(D_DA_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_da_dict[i]), 95)]]), axis=0)
#     D_FA_95 = np.append(D_FA_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_fa_dict[i]), 95)]]), axis=0)
#
#
#     #Foreign weights
#     # F_DC_mean = np.append(F_DC_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_dc_dict[i]))]]), axis=0)
#     # F_FC_mean = np.append(F_FC_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_fc_dict[i]))]]), axis=0)
#     # F_DA_mean = np.append(F_DA_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_da_dict[i]))]]), axis=0)
#     # F_FA_mean = np.append(F_FA_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_fa_dict[i]))]]), axis=0)
#     #
#     # F_DC_5 = np.append(F_DC_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_dc_dict[i]), 5)]]), axis=0)
#     # F_FC_5 = np.append(F_FC_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_fc_dict[i]), 5)]]), axis=0)
#     # F_DA_5 = np.append(F_DA_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_da_dict[i]), 5)]]), axis=0)
#     # F_FA_5 = np.append(F_FA_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_fa_dict[i]), 5)]]), axis=0)
#     #
#     # F_DC_95 = np.append(F_DC_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_dc_dict[i]), 95)]]),
#     #                     axis=0)
#     # F_FC_95 = np.append(F_FC_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_fc_dict[i]), 95)]]),
#     #                     axis=0)
#     # F_DA_95 = np.append(F_DA_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_da_dict[i]), 95)]]),
#     #                     axis=0)
#     # F_FA_95 = np.append(F_FA_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_fa_dict[i]), 95)]]),axis=0)
#
#
#
# ##Make Plots
#
# rc('text', usetex=True)
#
# fig, ax = plt.subplots()
# x=D_DA_mean[:,0]
# y=D_DA_mean[:,1]
#
# lists = sorted(itertools.izip(*[x, y]))
# new_x, new_y = list(itertools.izip(*lists))
# ax.plot(new_x, new_y,"-b", label='a')
#
# x=D_DA_5[:,0]
# y=D_DA_5[:,1]
#
# lists = sorted(itertools.izip(*[x, y]))
# new_x, new_y = list(itertools.izip(*lists))
# ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
#
# x=D_DA_95[:,0]
# y=D_DA_95[:,1]
#
# lists = sorted(itertools.izip(*[x, y]))
# new_x, new_y = list(itertools.izip(*lists))
# ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
# fig.show()
#

############ Look at weights #########
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
x=D_DC_mean[:,0]
y=D_DC_mean[:,1]
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
axes[0][0].plot(new_x, new_y,"-b", label='a')
x=D_DC_5[:,0]
y=D_DC_5[:,1]
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
axes[0][0].plot(new_x, new_y, linestyle='--',color='xkcd:grey')
x=D_DC_95[:,0]
y=D_DC_95[:,1]
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
axes[0][0].plot(new_x, new_y, linestyle='--',color='xkcd:grey')
axes[0][0].set_xlabel("x")
axes[0][0].set_ylabel('Domestic Fund: Domestic Cash')
axes[0][0].legend(loc='center right', frameon=False, labelspacing = 1.5)
#############################################
#######################
x=D_FC_mean[:,0]
y=D_FC_mean[:,1]
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
axes[0][1].plot(new_x, new_y,"-b", label='a')
x=D_FC_5[:,0]
y=D_FC_5[:,1]
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
axes[0][1].plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=D_FC_95[:,0]
y=D_FC_95[:,1]

lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
axes[0][1].plot(new_x, new_y, linestyle='--',color='xkcd:grey')
axes[0][1].set_xlabel("x")
axes[0][1].set_ylabel('Domestic Fund: Foreign Cash')
axes[0][1].legend(loc='upper center', frameon=False, labelspacing = 1.5)

#############################################
###################### domestic assets
x=D_DA_mean[:,0]
y=D_DA_mean[:,1]
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
axes[1][0].plot(new_x, new_y,"-b", label='a')

x=D_DA_5[:,0]
y=D_DA_5[:,1]
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
axes[1][0].plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=D_DA_95[:,0]
y=D_DA_95[:,1]
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))

axes[1][0].plot(new_x, new_y, linestyle='--',color='xkcd:grey')
axes[1][0].set_xlabel("x")
axes[1][0].set_ylabel('Domestic Fund: Domestic Asset')
axes[1][0].legend(loc='center right', frameon=False, labelspacing = 1.5)
#############################################
# foreign assets
#############################################
x=D_FA_mean[:,0]
y=D_FA_mean[:,1]
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
axes[1][1].plot(new_x, new_y,"-b", label='a')
x=D_FA_5[:,0]
y=D_FA_5[:,1]

lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
axes[1][1].plot(new_x, new_y, linestyle='--',color='xkcd:grey')
axes[1][1].set_xlabel("x")
axes[1][1].set_ylabel('Domestic Fund: Foreign Asset')

x=D_FA_95[:,0]
y=D_FA_95[:,1]
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
axes[1][1].plot(new_x, new_y, linestyle='--',color='xkcd:grey')
axes[1][1].legend(loc='center right', frameon=False, labelspacing = 1.5)
fig.show()
#
#
#
#
#
#
#
#
# #Market size vs FX rate
# #
# # fig, ax = plt.subplots()
# # x=FX_mean[:,0]
# # y=FX_mean[:,1]
# #
# # lists = sorted(itertools.izip(*[x, y]))
# #
# # new_x1m, new_y1m = list(itertools.izip(*lists))
# # ax.plot(new_x1m, new_y1m,"-b", label='a')
# #
# # x=FX_5[:,0]
# # y=FX_5[:,1]
# # lists = sorted(itertools.izip(*[x, y]))
# # new_x15, new_y15 = list(itertools.izip(*lists))
# # ax.plot(new_x15, new_y15, linestyle='--',color='xkcd:grey', label='b')
# #
# # x=FX_95[:,0]
# # y=FX_95[:,1]
# # lists = sorted(itertools.izip(*[x, y]))
# # new_x195, new_y195 = list(itertools.izip(*lists))
# # ax.plot(new_x195, new_y195,linestyle='--',color='xkcd:grey')
# # plt.xlabel("x")
# # plt.ylabel('y')
# # ax.legend(loc='upper center', frameon=False, labelspacing = 1.5)
# # #plt.savefig('marketsize_FX.eps', format="eps")
# # plt.show()
# #plt.close()
#
#
#
#
#
# ##########################
# ##############################
# #time series Prices
# ##############################
#
#
# x= p0_dict[obj_label1]
# x2= p1_dict[obj_label1]
#
# x3 = p0_dict[obj_label2]
# x4 =  p1_dict[obj_label2]
#
# x5 = p0_dict[obj_label3]
# x6 =  p1_dict[obj_label3]
# fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 6))
# axes[0][0].plot(x, '--', lw=2, ms=4.5, color='B', label="")
# axes[0][0].set_ylabel('p0')
#
#
# axes[1][0].plot(x2, '--', lw=2, ms=4.5, color='B', label="")
# axes[1][0].set_ylabel('p1')
# axes[1][0].set_xlabel(obj_label1)
#
# axes[0][1].plot(x3, '--', lw=2, ms=4.5, color='C', label="")
# axes[0][1].set_ylabel('p0')
#
#
# axes[1][1].plot(x4, '--', lw=2, ms=4.5, color='C', label="")
# axes[1][1].set_ylabel('p1')
# axes[1][1].set_xlabel(obj_label2)
#
#
# axes[0][2].plot(x5, '--', lw=2, ms=4.5, color='R', label="")
# axes[0][2].set_ylabel('p0')
#
#
# axes[1][2].plot(x6, '--', lw=2, ms=4.5, color='R', label="")
# axes[1][2].set_ylabel('p1')
# axes[1][2].set_xlabel(obj_label3)
#
# fig.show()
# ##############################
# ##############################
# ##############################
# ##############################
# #FX
# ##############################
# fx1 = fx_dict[obj_label1]
# fx2 = fx_dict[obj_label2]
# fx3 = fx_dict[obj_label3]
#
# fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 5), sharex=False, sharey=True)
# axes[0].plot(fx1, '--', lw=2, ms=4.5, color='B', label="")
# axes[0].set_ylabel('fx')
# axes[0].set_xlabel(obj_label1)
#
# axes[1].plot(fx2, '--', lw=2, ms=4.5, color='C', label="")
# axes[1].set_ylabel('fx')
# axes[1].set_xlabel(obj_label2)
#
# axes[2].plot(fx3, '--', lw=2, ms=4.5, color='R', label="")
# axes[2].set_ylabel('fx')
# axes[2].set_xlabel(obj_label3)
#
# fig.show()
# ##############################
# ##### Fund weights############
# ##############################
# #
#
# obj_label1 = 'Marketsize_0.5'
# obj_label2 = 'Marketsize_1'
# obj_label3 = 'Marketsize_2'
#
# x1_d_c0 = d_dc_dict[obj_label1]
# x1_d_c1 = d_fc_dict[obj_label1]
# x1_d_a0 = d_da_dict[obj_label1]
# x1_d_a1 = d_da_dict[obj_label1]
#
# fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 10),  sharex=True, sharey=True)  # sharex=False, sharey=True
#
# import matplotlib.gridspec as gridspec
# gs = gridspec.GridSpec(2, 4)
# gs.update(wspace=0.5)
# axes[0] = plt.subplot(gs[0, :2], )
# axes[1] = plt.subplot(gs[0, 2:])
# axes[2] = plt.subplot(gs[1, 1:3])
#
# axes[0].plot(x1_d_c0, 'bo'  , lw=2, ms=4.5, label="d_domestic_cash")
# axes[0].plot(  x1_d_c1 ,  '--', lw=2, ms=4.5, color='R', label="d_foreign_cash")
# axes[0].plot(  x1_d_a0 ,  '-', lw=2, ms=4.5, color='C', label="d_domestic")
# axes[0].plot(  x1_d_a1 ,  'v', lw=2, ms=4.5, color='purple', label="d_foreign")
#
# #axes[0].set_ylabel('fund_weights domestic fund')
# axes[0].set_xlabel(str(obj_label1))
#  #
# x2_d_c0 = d_dc_dict[obj_label2]
# x2_d_c1 = d_fc_dict[obj_label2]
# x2_d_a0 = d_da_dict[obj_label2]
# x2_d_a1 = d_fa_dict[obj_label2]
# axes[1].plot(x2_d_c0, 'bo'  , lw=2, ms=4.5, label="d_domestic_cash")
# axes[1].plot(  x2_d_c1 ,  '--', lw=2, ms=4.5, color='R', label="d_foreign_cash")
# #axes[1].set_xlabel(str(obj_label2))
# axes[1].plot(  x2_d_a0 ,  '-', lw=2, ms=4.5, color='C', label="d_domestic")
# axes[1].plot(  x2_d_a1 ,  'v', lw=2, ms=4.5, color='purple', label="d_foreign")
#
# #
# x3_d_c0 = d_dc_dict[obj_label3]
# x3_d_c1 = d_fc_dict[obj_label3]
# x3_d_a0 = d_da_dict[obj_label3]
# x3_d_a1 = d_fa_dict[obj_label3]
# axes[2].plot(x3_d_c0, 'bo'  , lw=2, ms=4.5, label="d_domestic_cash")
# axes[2].plot(  x3_d_c1 ,  '--', lw=2, ms=4.5, color='R', label="d_foreign_cash")
# axes[2].plot(  x3_d_a0 ,  '-', lw=2, ms=4.5, color='C', label="d_domestic")
# axes[2].plot(  x3_d_a1 ,  'v', lw=2, ms=4.5, color='purple', label="d_foreign")
# axes[2].legend(loc='best')
# #axes[2].set_xlabel(str(obj_label3))
#
# #legend
# box = axes[2].get_position()
# axes[2].set_position([box.x0, box.y0, box.width , box.height])
# axes[2].legend(loc='upper left', bbox_to_anchor=(1.1, 0.99))
#
# plt.show()
##############################