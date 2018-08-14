import  pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools

################    #################    #################
#################    time-series    #################
#################    #################    #################
#Execute selection of code (possible in pycharm, unpickling .pkl in jupyter yields import error)
local_dir = "/Users/Tina/git_repos/qe-financial-spillover/Experiments/Marketsize/Objects_marketsize/"

#local_dir = "Objects_marketsize/"

variable = [0.5, 1, 2]
obj_label1 = 'Marketsize0.5'
obj_label2 = 'Marketsize1'
obj_label3 = 'Marketsize2'

fx_dict = {}
p0_dict = {}
p1_dict = {}

d_ra0_dict = {}
d_ra1_dict = {}

f_ra0_dict = {}
f_ra1_dict = {}

d_rc0_dict = {}
d_rc1_dict = {}

f_rc0_dict = {}
f_rc1_dict = {}

f_q0_dict = {}
f_q1_dict = {}
d_q0_dict = {}
d_q1_dict = {}

hb_d_dict = {}
hb_f_dict = {}

d_c0_dict = {}
d_c1_dict = {}
d_a0_dict = {}
d_a1_dict = {}

f_c0_dict = {}
f_c1_dict = {}
f_a0_dict = {}
f_a1_dict = {}



for i in variable:
    obj_label =  "Marketsize" + str(i)

    #variables to extract

    fx = []
    p0 = []
    p1 = []

    d_ra0 = []
    d_ra1 = []

    f_ra0 = []
    f_ra1 = []

    d_rc0 = []
    d_rc1 = []

    f_rc0 = []
    f_rc1 = []

    f_q0 = []
    f_q1 = []
    d_q0 = []
    d_q1 = []

    hb_d = []
    hb_f = []

    d_c0 = []
    d_c1 = []
    d_a0 = []
    d_a1 = []

    f_c0 = []
    f_c1 = []
    f_a0 = []
    f_a1 = []


    for day in range(1,5000):
        filename = local_dir + "objects_day_" + str(day) + "_seed_1_"  + obj_label+".pkl"
        data = open(filename,"rb")
        list_of_objects = pickle.load(data)

        portfolios = list_of_objects[0]
        currencies = list_of_objects[1]
        environment = list_of_objects[2]
        exogeneous_agents = list_of_objects[3]
        funds = list_of_objects[4]

        fx.append(environment.var.fx_rates.iloc[0,1])
        p0.append(portfolios[0].var.price)
        p1.append(portfolios[1].var.price)

        d_ra1.append(funds[0].exp.returns[portfolios[1]])
        d_ra0.append(funds[0].exp.returns[portfolios[0]])

        f_ra1.append(funds[1].exp.returns[portfolios[1]])
        f_ra0.append(funds[1].exp.returns[portfolios[0]])

        d_rc1.append(funds[0].exp.returns[currencies[1]])
        d_rc0.append(funds[0].exp.returns[currencies[0]])

        f_rc1.append(funds[1].exp.returns[currencies[1]])
        f_rc0.append(funds[1].exp.returns[currencies[0]])

        d_q1.append(funds[0].var.assets[portfolios[1]])
        d_q0.append(funds[0].var.assets[portfolios[0]])
        f_q1.append(funds[1].var.assets[portfolios[1]])
        f_q0.append(funds[1].var.assets[portfolios[0]])

        hb_d.append(funds[0].var.weights[portfolios[1]] + funds[0].var.weights[currencies[1]])
        hb_f.append(funds[1].var.weights[portfolios[0]] + funds[1].var.weights[currencies[0]])

        d_c0.append(funds[0].var.weights[currencies[0]])
        d_c1.append(funds[0].var.weights[currencies[1]])
        d_a0.append(funds[0].var.weights[portfolios[0]])
        d_a1.append(funds[0].var.weights[portfolios[1]])

        f_c0.append(funds[1].var.weights[currencies[0]])
        f_c1.append(funds[1].var.weights[currencies[1]])
        f_a0.append(funds[1].var.weights[portfolios[0]])
        f_a1.append(funds[1].var.weights[portfolios[1]])
        print day
#################    #################    #################
#################    #################    #################
#################    #################    #################
	
	fx_dict.update({obj_label: fx})
    p0_dict.update({obj_label: p0})
    p1_dict.update({obj_label: p1})

    d_ra0_dict.update({obj_label: d_ra0})
    d_ra1_dict.update({obj_label: d_ra1})

    f_ra0_dict.update({obj_label: f_ra0})
    f_ra1_dict.update({obj_label: f_ra1})

    d_rc0_dict.update({obj_label: d_rc0})
    d_rc1_dict.update({obj_label: d_rc1})

    f_rc0_dict.update({obj_label: f_rc0})
    f_rc1_dict.update({obj_label: f_rc1})

    hb_d_dict.update({obj_label: hb_d})
    hb_f_dict.update({obj_label: hb_f})

    d_c0_dict.update({obj_label: d_c0})
    d_c1_dict.update({obj_label: d_c1})
    d_a0_dict.update({obj_label: d_a0})
    d_a1_dict.update({obj_label: d_a1})

    f_c0_dict.update({obj_label: f_c0})
    f_c1_dict.update({obj_label: f_c1})
    f_a0_dict.update({obj_label: f_a0})
    f_a1_dict.update({obj_label: f_a1})

    d_q0_dict.update({obj_label: d_q0})
    d_q1_dict.update({obj_label: d_q1})
    f_q0_dict.update({obj_label: f_q0})
    f_q1_dict.update({obj_label: f_q1})




##############################
#Prices
##############################
x= p0_dict[obj_label1]
x2= p1_dict[obj_label1]

x3 = p0_dict[obj_label2]
x4 =  p1_dict[obj_label2]

x5 = p0_dict[obj_label3]
x6 =  p1_dict[obj_label3]
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 6))
axes[0][0].plot(x, '--', lw=2, ms=4.5, color='B', label="")
axes[0][0].set_ylabel('p0')


axes[1][0].plot(x2, '--', lw=2, ms=4.5, color='B', label="")
axes[1][0].set_ylabel('p1')
axes[1][0].set_xlabel(obj_label1)

axes[0][1].plot(x3, '--', lw=2, ms=4.5, color='C', label="")
axes[0][1].set_ylabel('p0')


axes[1][1].plot(x4, '--', lw=2, ms=4.5, color='C', label="")
axes[1][1].set_ylabel('p1')
axes[1][1].set_xlabel(obj_label2)


axes[0][2].plot(x5, '--', lw=2, ms=4.5, color='R', label="")
axes[0][2].set_ylabel('p0')


axes[1][2].plot(x6, '--', lw=2, ms=4.5, color='R', label="")
axes[1][2].set_ylabel('p1')
axes[1][2].set_xlabel(obj_label3)

fig.show()
##############################
##############################
##############################


##############################
#FX
##############################
fx1 = fx_dict[obj_label1]
fx2 = fx_dict[obj_label2]
fx3 = fx_dict[obj_label3]

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 5), sharex=False, sharey=True)
axes[0].plot(fx1, '--', lw=2, ms=4.5, color='B', label="")
axes[0].set_ylabel('fx')
axes[0].set_xlabel(obj_label1)


axes[1].plot(fx2, '--', lw=2, ms=4.5, color='C', label="")
axes[1].set_ylabel('fx')
axes[1].set_xlabel(obj_label2)


axes[2].plot(fx3, '--', lw=2, ms=4.5, color='R', label="")
axes[2].set_ylabel('fx')
axes[2].set_xlabel(obj_label3)

fig.show()
##############################
##### Fund weights############
##############################
#


x1_d_c0 = d_c0_dict[obj_label1]
x1_d_c1 = d_c1_dict[obj_label1]
x1_d_a0 = d_a0_dict[obj_label1]
x1_d_a1 = d_a1_dict[obj_label1]

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 5),  sharex=True, sharey=True)  # sharex=False, sharey=True
axes[0].plot(x1_d_c0, 'bo'  , lw=2, ms=4.5, label="d_domestic_cash")
axes[0].plot(  x1_d_c1 ,  '--', lw=2, ms=4.5, color='R', label="d_foreign_cash")
axes[0].plot(  x1_d_a0 ,  '-', lw=2, ms=4.5, color='C', label="d_domestic")
axes[0].plot(  x1_d_a1 ,  'v', lw=2, ms=4.5, color='purple', label="d_foreign")

axes[0].set_ylabel('fund_weights domestic fund')
axes[0].set_xlabel(obj_label1)
axes[0].legend(loc='best')
#
x2_d_c0 = d_c0_dict[obj_label2]
x2_d_c1 = d_c1_dict[obj_label2]
x2_d_a0 = d_a0_dict[obj_label2]
x2_d_a1 = d_a1_dict[obj_label2]
axes[1].plot(x2_d_c0, 'bo'  , lw=2, ms=4.5, label="d_domestic_cash")
axes[1].plot(  x2_d_c1 ,  '--', lw=2, ms=4.5, color='R', label="d_foreign_cash")
axes[1].set_xlabel(obj_label2)
axes[1].plot(  x2_d_a0 ,  '-', lw=2, ms=4.5, color='C', label="d_domestic")
axes[1].plot(  x2_d_a1 ,  'v', lw=2, ms=4.5, color='purple', label="d_foreign")
axes[1].legend(loc='best')

#

x3_d_c0 = d_c0_dict[obj_label3]
x3_d_c1 = d_c1_dict[obj_label3]
x3_d_a0 = d_a0_dict[obj_label3]
x3_d_a1 = d_a1_dict[obj_label3]
axes[2].plot(x3_d_c0, 'bo'  , lw=2, ms=4.5, label="d_domestic_cash")
axes[2].plot(  x3_d_c1 ,  '--', lw=2, ms=4.5, color='R', label="d_foreign_cash")
axes[2].plot(  x3_d_a0 ,  '-', lw=2, ms=4.5, color='C', label="d_domestic")
axes[2].plot(  x3_d_a1 ,  'v', lw=2, ms=4.5, color='purple', label="d_foreign")
axes[2].legend(loc='best')
axes[2].set_xlabel(obj_label3)

fig.show()







##############################
##############################


delta_fx = {}
delta_hb_d = {}
delta_hb_f = {}


delta_d_c0 = {}
delta_d_c1 = {}
delta_d_a0 = {}
delta_d_a1 = {}

delta_rfx = {}


delta_f_c0 = {}
delta_f_c1 = {}
delta_f_a0 = {}
delta_f_a1 = {}


delta_d_ra0 = {}
delta_d_ra1 = {}


FX =np.empty((0,2), float)
R_FX=np.empty((0,2), float)
R_FX_mean = np.empty((0,2), float)
R_FX_5 =np.empty((0,2), float)
R_FX_95 =np.empty((0,2), float)



P0_mean = np.empty((0,2), float)
P0_5 =np.empty((0,2), float)
P0_95 =np.empty((0,2), float)

P1_mean = np.empty((0,2), float)
P1_5 =np.empty((0,2), float)
P1_95 =np.empty((0,2), float)



D_DC_mean = np.empty((0,2), float)
D_DC_5 =np.empty((0,2), float)
D_DC_95 =np.empty((0,2), float)

D_FC_mean = np.empty((0,2), float)
D_FC_5 =np.empty((0,2), float)
D_FC_95 =np.empty((0,2), float)

D_DA_mean = np.empty((0,2), float)
D_DA_5 =np.empty((0,2), float)
D_DA_95 =np.empty((0,2), float)

D_FA_mean = np.empty((0,2), float)
D_FA_5 =np.empty((0,2), float)
D_FA_95 =np.empty((0,2), float)

F_DC_mean = np.empty((0,2), float)
F_DC_5 =np.empty((0,2), float)
F_DC_95 =np.empty((0,2), float)

F_FC_mean = np.empty((0,2), float)
F_FC_5 =np.empty((0,2), float)
F_FC_95 =np.empty((0,2), float)

F_DA_mean = np.empty((0,2), float)
F_DA_5 =np.empty((0,2), float)
F_DA_95 =np.empty((0,2), float)

F_FA_mean = np.empty((0,2), float)
F_FA_5 =np.empty((0,2), float)
F_FA_95 =np.empty((0,2), float)



D_Q0_mean =np.empty((0,2), float)
D_Q1_mean =np.empty((0,2), float)
D_Q0_5 =np.empty((0,2), float)
D_Q1_5 =np.empty((0,2), float)
D_Q0_95 =np.empty((0,2), float)
D_Q1_95 =np.empty((0,2), float)
F_Q0_mean=np.empty((0,2), float)
F_Q1_mean=np.empty((0,2), float)
F_Q0_5=np.empty((0,2), float)
F_Q1_5=np.empty((0,2), float)
F_Q0_95=np.empty((0,2), float)
F_Q1_95=np.empty((0,2), float)


D_R0_mean = np.empty((0, 2), float)
D_R1_mean = np.empty((0, 2), float)
D_R0_5 = np.empty((0, 2), float)
D_R1_5 = np.empty((0, 2), float)
D_R0_95 = np.empty((0, 2), float)
D_R1_95 = np.empty((0, 2), float)

F_R0_mean = np.empty((0, 2), float)
F_R1_mean = np.empty((0, 2), float)
F_R0_5 = np.empty((0, 2), float)
F_R1_5 = np.empty((0, 2), float)
F_R0_95 = np.empty((0, 2), float)
F_R1_95 = np.empty((0, 2), float)


FX_mean =np.empty((0,2), float)
FX_5 =np.empty((0,2), float)
FX_95 =np.empty((0,2), float)


for i in fx_dict:
    f0 =np.array(fx_dict['QE_asset_target_0'])
    f=  np.array(fx_dict[i])
    FX_mean=np.append(FX_mean, np.array([[float(i.split("_")[-1]),np.mean(f/f0-1)]]),axis=0)
    FX_5 = np.append(FX_5, np.array([[float(i.split("_")[-1]), np.percentile(f/f0-1, 5)]]), axis=0)
    FX_95 = np.append(FX_95, np.array([[float(i.split("_")[-1]), np.percentile(f/f0-1, 95)]]), axis=0)

    P00 =np.array(p0_dict['QE_asset_target_0'])
    P0=  np.array(p0_dict[i])
    P0_mean=np.append(P0_mean, np.array([[float(i.split("_")[-1]),np.mean(P0/P00-1)]]),axis=0)
    P0_5 = np.append(P0_5, np.array([[float(i.split("_")[-1]), np.percentile(P0/P00-1, 5)]]), axis=0)
    P0_95 = np.append(P0_95, np.array([[float(i.split("_")[-1]), np.percentile(P0/P00-1, 95)]]), axis=0)

    P10 =np.array(p1_dict['QE_asset_target_0'])
    P1=  np.array(p1_dict[i])
    P1_mean=np.append(P1_mean, np.array([[float(i.split("_")[-1]),np.mean(P1/P10-1)]]),axis=0)
    P1_5 = np.append(P1_5, np.array([[float(i.split("_")[-1]), np.percentile(P1/P10-1, 5)]]), axis=0)
    P1_95 = np.append(P1_95, np.array([[float(i.split("_")[-1]), np.percentile(P1/P10-1, 95)]]), axis=0)




    d_ys_r0= np.divide(np.array(d_ra0_dict[i]) - np.array(d_rc0_dict[i]),np.array(d_ra0_dict['QE_asset_target_0']) - np.array(d_rc0_dict['QE_asset_target_0']))-1
    d_ys_r1= np.divide(np.array(d_ra1_dict[i]) - np.array(d_rc1_dict[i]),np.array(d_ra1_dict['QE_asset_target_0']) - np.array(d_rc1_dict['QE_asset_target_0']))-1
    f_ys_r0= np.divide(np.array(f_ra0_dict[i]) - np.array(f_rc0_dict[i]),np.array(f_ra0_dict['QE_asset_target_0']) - np.array(f_rc0_dict['QE_asset_target_0']))-1
    f_ys_r1= np.divide(np.array(f_ra1_dict[i]) - np.array(f_rc1_dict[i]),np.array(f_ra1_dict['QE_asset_target_0']) - np.array(f_rc1_dict['QE_asset_target_0']))-1


    d_ys_r0= (np.array(d_ra0_dict[i]) - np.array(d_rc0_dict[i]))-(np.array(d_ra0_dict['QE_asset_target_0']) - np.array(d_rc0_dict['QE_asset_target_0']))
    d_ys_r1= (np.array(d_ra1_dict[i]) - np.array(d_rc1_dict[i]))-(np.array(d_ra1_dict['QE_asset_target_0']) - np.array(d_rc1_dict['QE_asset_target_0']))
    f_ys_r0= (np.array(f_ra0_dict[i]) - np.array(f_rc0_dict[i]))-(np.array(f_ra0_dict['QE_asset_target_0']) - np.array(f_rc0_dict['QE_asset_target_0']))
    f_ys_r1= (np.array(f_ra1_dict[i]) - np.array(f_rc1_dict[i]))-(np.array(f_ra1_dict['QE_asset_target_0']) - np.array(f_rc1_dict['QE_asset_target_0']))




    D_R0_mean=np.append(D_R0_mean, np.array([[float(i.split("_")[-1]), np.mean(d_ys_r0)]]), axis=0)
    D_R1_mean=np.append(D_R1_mean, np.array([[float(i.split("_")[-1]), np.mean(d_ys_r1)]]), axis=0)
    D_R0_5 = np.append(D_R0_5, np.array([[float(i.split("_")[-1]), np.percentile(d_ys_r0, 5)]]), axis=0)
    D_R1_5 = np.append(D_R1_5, np.array([[float(i.split("_")[-1]), np.percentile(d_ys_r1, 5)]]), axis=0)
    D_R0_95 = np.append(D_R0_95, np.array([[float(i.split("_")[-1]), np.percentile(d_ys_r0, 95)]]), axis=0)
    D_R1_95 = np.append(D_R1_95, np.array([[float(i.split("_")[-1]), np.percentile(d_ys_r1, 95)]]), axis=0)

    F_R0_mean=np.append(F_R0_mean, np.array([[float(i.split("_")[-1]), np.mean(f_ys_r0)]]), axis=0)
    F_R1_mean=np.append(F_R1_mean, np.array([[float(i.split("_")[-1]), np.mean(f_ys_r1)]]), axis=0)
    F_R0_5 = np.append(F_R0_5, np.array([[float(i.split("_")[-1]), np.percentile(f_ys_r0, 5)]]), axis=0)
    F_R1_5 = np.append(F_R1_5, np.array([[float(i.split("_")[-1]), np.percentile(f_ys_r1, 5)]]), axis=0)
    F_R0_95 = np.append(F_R0_95, np.array([[float(i.split("_")[-1]), np.percentile(f_ys_r0, 95)]]), axis=0)
    F_R1_95 = np.append(F_R1_95, np.array([[float(i.split("_")[-1]), np.percentile(f_ys_r1, 95)]]), axis=0)


    delta_fx.update({i: np.multiply(((np.array(fx_dict[i])/np.array(fx_dict['QE_asset_target_0']))-1),100)})
    delta_hb_d.update({i: np.multiply(((np.array(hb_d_dict[i])/np.array(hb_d_dict['QE_asset_target_0']))-1),100)})
    delta_hb_f.update({i: np.multiply(((np.array(hb_f_dict[i])/np.array(hb_f_dict['QE_asset_target_0']))-1),100)})


    delta_d_c0.update({i: np.multiply(((np.array(d_c0_dict[i]) / np.array(d_c0_dict['QE_asset_target_0'])) - 1), 100)})
    delta_d_a0.update({i: np.multiply(((np.array(d_a0_dict[i]) / np.array(d_a0_dict['QE_asset_target_0'])) - 1), 100)})
    delta_d_c1.update({i: np.multiply(((np.array(d_c1_dict[i]) / np.array(d_c1_dict['QE_asset_target_0'])) - 1), 100)})
    delta_d_a1.update({i: np.multiply(((np.array(d_a1_dict[i]) / np.array(d_a1_dict['QE_asset_target_0'])) - 1), 100)})

    delta_f_c0.update({i: np.multiply(((np.array(f_c0_dict[i])/np.array(f_c0_dict['QE_asset_target_0']))-1),100)})
    delta_f_a0.update({i: np.multiply(((np.array(f_a0_dict[i])/np.array(f_a0_dict['QE_asset_target_0']))-1),100)})
    delta_f_c1.update({i: np.multiply(((np.array(f_c1_dict[i])/np.array(f_c1_dict['QE_asset_target_0']))-1),100)})
    delta_f_a1.update({i: np.multiply(((np.array(f_a1_dict[i])/np.array(f_a1_dict['QE_asset_target_0']))-1),100)})


    delta_d_ra0.update({i: np.multiply((((np.array(d_ra0_dict[i])-np.array(d_rc0_dict[i])) / (np.array(d_ra0_dict['QE_asset_target_0'])-np.array(d_rc0_dict['QE_asset_target_0'])))-1),100)})
    delta_d_ra1.update({i: np.multiply((((np.array(d_ra1_dict[i])-np.array(d_rc1_dict[i])) / (np.array(d_ra1_dict['QE_asset_target_0'])-np.array(d_rc1_dict['QE_asset_target_0'])))-1),100)})

    delta_rfx.update({i: (np.array(d_rc1_dict[i])-np.array(f_rc1_dict[i]))})


    D_DC_mean = np.append(D_DC_mean, np.array([[float(i.split("_")[-1]),np.mean(np.array(d_c0_dict[i]))]]),axis=0)
    D_FC_mean = np.append(D_FC_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_c1_dict[i]))]]), axis=0)
    D_DA_mean = np.append(D_DA_mean, np.array([[float(i.split("_")[-1]),np.mean(np.array(d_a0_dict[i]))]]),axis=0)
    D_FA_mean = np.append(D_FA_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_a1_dict[i]))]]), axis=0)

    D_DC_5 = np.append(D_DC_5, np.array([[float(i.split("_")[-1]),np.percentile(np.array(d_c0_dict[i]),5)]]),axis=0)
    D_FC_5 = np.append(D_FC_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_c1_dict[i]),5)]]), axis=0)
    D_DA_5 = np.append(D_DA_5, np.array([[float(i.split("_")[-1]),np.percentile(np.array(d_a0_dict[i]),5)]]),axis=0)
    D_FA_5 = np.append(D_FA_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_a1_dict[i]),5)]]), axis=0)

    D_DC_95 = np.append(D_DC_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(d_c0_dict[i]),95)]]),axis=0)
    D_FC_95 = np.append(D_FC_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(d_c1_dict[i]),95)]]), axis=0)
    D_DA_95 = np.append(D_DA_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(d_a0_dict[i]),95)]]),axis=0)
    D_FA_95 = np.append(D_FA_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(d_a1_dict[i]),95)]]), axis=0)

    F_DC_mean = np.append(F_DC_mean, np.array([[float(i.split("_")[-1]),np.mean(np.array(f_c0_dict[i]))]]),axis=0)
    F_FC_mean = np.append(F_FC_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_c1_dict[i]))]]), axis=0)
    F_DA_mean = np.append(F_DA_mean, np.array([[float(i.split("_")[-1]),np.mean(np.array(f_a0_dict[i]))]]),axis=0)
    F_FA_mean = np.append(F_FA_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_a1_dict[i]))]]), axis=0)

    F_DC_5 = np.append(F_DC_5, np.array([[float(i.split("_")[-1]),np.percentile(np.array(f_c0_dict[i]),5)]]),axis=0)
    F_FC_5 = np.append(F_FC_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_c1_dict[i]),5)]]), axis=0)
    F_DA_5 = np.append(F_DA_5, np.array([[float(i.split("_")[-1]),np.percentile(np.array(f_a0_dict[i]),5)]]),axis=0)
    F_FA_5 = np.append(F_FA_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_a1_dict[i]),5)]]), axis=0)

    F_DC_95 = np.append(F_DC_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(f_c0_dict[i]),95)]]),axis=0)
    F_FC_95 = np.append(F_FC_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(f_c1_dict[i]),95)]]), axis=0)
    F_DA_95 = np.append(F_DA_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(f_a0_dict[i]),95)]]),axis=0)
    F_FA_95 = np.append(F_FA_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(f_a1_dict[i]),95)]]), axis=0)


    D_Q0_mean=np.append(D_Q0_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_q0_dict[i]))]]), axis=0)
    D_Q1_mean=np.append(D_Q1_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_q1_dict[i]))]]), axis=0)
    D_Q0_5 = np.append(D_Q0_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_q0_dict[i]), 5)]]), axis=0)
    D_Q1_5 = np.append(D_Q1_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_q1_dict[i]), 5)]]), axis=0)
    D_Q0_95 = np.append(D_Q0_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_q0_dict[i]), 95)]]), axis=0)
    D_Q1_95 = np.append(D_Q1_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_q1_dict[i]), 95)]]), axis=0)

    F_Q0_mean=np.append(F_Q0_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_q0_dict[i]))]]), axis=0)
    F_Q1_mean=np.append(F_Q1_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_q1_dict[i]))]]), axis=0)
    F_Q0_5 = np.append(F_Q0_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_q0_dict[i]), 5)]]), axis=0)
    F_Q1_5 = np.append(F_Q1_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_q1_dict[i]), 5)]]), axis=0)
    F_Q0_95 = np.append(F_Q0_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_q0_dict[i]), 95)]]), axis=0)
    F_Q1_95 = np.append(F_Q1_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_q1_dict[i]), 95)]]), axis=0)



rc('text', usetex=True)

fig, ax = plt.subplots()
x = np.divide(range(0,len(fx_dict["QE_asset_target_0"])),20.8333)
ax.plot(x, delta_fx["QE_asset_target_20"],"-b", label='a')
ax.plot(x, delta_fx["QE_asset_target_100"],"--r", label='b')
ax.plot(x, delta_fx["QE_asset_target_500"],"-.g", label='c')
ax.set_xlabel("x")
ax.set_ylabel('y')
ax.legend(loc='upper left', frameon=False, labelspacing = 1.5)
plt.savefig('qe_fx_impact_ts.eps', format="eps")
plt.close()

fig, ax = plt.subplots()
x = np.divide(range(0,len(fx_dict["QE_asset_target_0"])),20.8333)
ax.plot(x, delta_rfx["QE_asset_target_20"],"-b", label='a')
ax.plot(x, delta_rfx["QE_asset_target_100"],"--r", label='b')
ax.plot(x, delta_rfx["QE_asset_target_500"],"-.g", label='c')
ax.set_xlabel("x")
ax.set_ylabel('y')
ax.legend(loc='upper left', frameon=False, labelspacing = 1.5)
#plt.savefig('qe_fx_impact_ts.eps', format="eps")
#plt.close()




fig, ax = plt.subplots()
x = np.divide(range(0,len(d_ra0_dict["QE_asset_target_0"])),20.8333)
ax.plot(x, delta_d_ra0["QE_asset_target_20"],"-b", label='a')
ax.plot(x, delta_d_ra0["QE_asset_target_100"],"--r", label='b')
ax.plot(x, delta_d_ra0["QE_asset_target_500"],"-.g", label='c')
ax.set_xlabel("x")
ax.set_ylabel('y')
ax.legend(loc='upper left', frameon=False, labelspacing = 1.5)
plt.savefig('qe_excess_ret0_ts.eps', format="eps")
plt.close()

fig, ax = plt.subplots()
x = np.divide(range(0,len(fx_dict["QE_asset_target_0"])),20.8333)
ax.plot(x, delta_d_ra1["QE_asset_target_20"],"-b", label='a')
ax.plot(x, delta_d_ra1["QE_asset_target_100"],"--r", label='b')
ax.plot(x, delta_d_ra1["QE_asset_target_500"],"-.g", label='c')
ax.set_xlabel("x")
ax.set_ylabel('y')
ax.legend(loc='upper left', frameon=False, labelspacing = 1.5)
plt.savefig('qe_excess_ret1_ts.eps', format="eps")
plt.close()





fig, ax = plt.subplots()
x=D_DC_mean[:,0]
y=D_DC_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-b", label='a')

x=D_DC_5[:,0]
y=D_DC_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=D_DC_95[:,0]
y=D_DC_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')



x=F_DC_mean[:,0]
y=F_DC_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-r", label='b')

x=F_DC_5[:,0]
y=F_DC_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label='c')

x=F_DC_95[:,0]
y=F_DC_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='upper left', frameon=False, labelspacing = 1.5)
plt.savefig('qe_domestic_cash_delta.eps', format="eps")
plt.close()



fig, ax = plt.subplots()
x=D_DA_mean[:,0]
y=D_DA_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-b", label='a')

x=D_DA_5[:,0]
y=D_DA_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=D_DA_95[:,0]
y=D_DA_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')



x=F_DA_mean[:,0]
y=F_DA_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-r", label='b')

x=F_DA_5[:,0]
y=F_DA_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label='c')

x=F_DA_95[:,0]
y=F_DA_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='lower left', frameon=False, labelspacing = 1.5)
plt.savefig('qe_domestic_asset_delta.eps', format="eps")
plt.close()







fig, ax = plt.subplots()
x=D_FC_mean[:,0]
y=D_FC_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-b", label='a')

x=D_FC_5[:,0]
y=D_FC_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=D_FC_95[:,0]
y=D_FC_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')



x=F_FC_mean[:,0]
y=F_FC_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-r", label='b')

x=F_FC_5[:,0]
y=F_FC_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label='c')

x=F_FC_95[:,0]
y=F_FC_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='center left', frameon=False, labelspacing = 1.5)
plt.savefig('qe_foreign_cash_delta.eps', format="eps")
plt.close()



fig, ax = plt.subplots()
x=D_FA_mean[:,0]
y=D_FA_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-b", label='a')

x=D_FA_5[:,0]
y=D_FA_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=D_FA_95[:,0]
y=D_FA_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')



x=F_FA_mean[:,0]
y=F_FA_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-r", label='b')

x=F_FA_5[:,0]
y=F_FA_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label='c')

x=F_FA_95[:,0]
y=F_FA_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='center left', frameon=False, labelspacing = 1.5)
plt.savefig('qe_foreign_asset_delta.eps', format="eps")
plt.close()





fig, ax = plt.subplots()
x=D_Q1_mean[:,0]
y=D_Q1_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-b", label='a')

x=D_Q1_5[:,0]
y=D_Q1_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=D_Q1_95[:,0]
y=D_Q1_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')



x=F_Q1_mean[:,0]
y=F_Q1_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-r", label='b')

x=F_Q1_5[:,0]
y=F_Q1_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label='c')

x=F_Q1_95[:,0]
y=F_Q1_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='center left', frameon=False, labelspacing = 1.5)
#plt.savefig('qe_foreign_asset_holdings.eps', format="eps")
plt.close()





fig, ax = plt.subplots()
x=D_R0_mean[:,0]
y=D_R0_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100*100*250)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-b", label='a')

x=D_R0_5[:,0]
y=D_R0_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100*100*250)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=D_R0_95[:,0]
y=D_R0_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100*100*250)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label="c")
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='lower_left', frameon=False, labelspacing = 1.5)
plt.savefig('qe_d_ex_return.eps', format="eps")
plt.close()


fig, ax = plt.subplots()
x=D_R1_mean[:,0]
y=D_R1_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100*100*250)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-b", label='a')

x=D_R1_5[:,0]
y=D_R1_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100*100*250)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=D_R1_95[:,0]
y=D_R1_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100*100*250)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label="c")
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc="lower left", frameon=False, labelspacing = 1.5)
plt.savefig('qe_f_ex_return.eps', format="eps")
plt.close()



fig, ax = plt.subplots()
x=FX_mean[:,0]
y=FX_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-b", label='a')

x=FX_5[:,0]
y=FX_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=FX_95[:,0]
y=FX_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label="c")
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc="upper left", frameon=False, labelspacing = 1.5)
plt.savefig('qe_fx.eps', format="eps")
plt.close()



fig, ax = plt.subplots()
x=P0_mean[:,0]
y=P0_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-b", label='a')

x=P0_5[:,0]
y=P0_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=P0_95[:,0]
y=P0_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label="c")
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='upper center', frameon=False, labelspacing = 1.5)
#plt.savefig('qe_d_ex_return.eps', format="eps")
#plt.close()


fig, ax = plt.subplots()
x=P1_mean[:,0]
y=P1_mean[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100) # percent
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-b", label='a')

x=P1_5[:,0]
y=P1_5[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=P1_95[:,0]
y=P1_95[:,1]
x=np.divide(x,50) # divide by 5000 multiply by 100
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label="c")
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc="upper left", frameon=False, labelspacing = 1.5)
#plt.savefig('qe_f_ex_return.eps', format="eps")
#plt.close()
