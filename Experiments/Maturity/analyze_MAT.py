import  pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools
import pandas as pd
from matplotlib.ticker import ScalarFormatter


local_dir = "Objects_MAT/"

variable = [0.952,0.984, 0.996, 0.9987,0.9992,0.9996,0.999733,0.9998,0.999867,0.9999,1]

fx_dict = {}

d_ra0_dict = {}
d_ra1_dict = {}

f_ra0_dict = {}
f_ra1_dict = {}

d_rc0_dict = {}
d_rc1_dict = {}


f_q0_dict = {}
f_q1_dict = {}
d_q0_dict = {}
d_q1_dict = {}

f_c0_dict = {}
f_c1_dict = {}
d_c0_dict = {}
d_c1_dict = {}



f_rc0_dict = {}
f_rc1_dict = {}

hb_d_dict = {}
hb_f_dict = {}

d_dc_dict = {}
d_fc_dict = {}
d_da_dict = {}
d_fa_dict = {}

f_dc_dict = {}
f_fc_dict = {}
f_da_dict = {}
f_fa_dict = {}

cov_11_dict = {}
cov_00_dict = {}
cov_01_dict = {}



for i in variable:
    obj_label =  "mat_" + str(i)


    #variables to extract

    fx = []

    d_ra0 = []
    d_ra1 = []

    f_ra0 = []
    f_ra1 = []

    d_rc0 = []
    d_rc1 = []


    f_q0 = []
    f_q1 = []
    d_q0 = []
    d_q1 = []

    f_c0 = []
    f_c1 = []
    d_c0 = []
    d_c1 = []

    f_rc0 = []
    f_rc1 = []

    hb_d = []
    hb_f = []

    d_dc = []
    d_fc = []
    d_da = []
    d_fa = []

    f_dc = []
    f_fc = []
    f_da = []
    f_fa = []

    cov_00 = []
    cov_11 = []
    cov_01 = []


    for day in range(4000,4999):
        filename = local_dir + "objects_day_" + str(day) + "_seed_1_"  + obj_label+".pkl"
        data = open(filename,"rb")
        list_of_objects = pickle.load(data)

        portfolios = list_of_objects[0]
        currencies = list_of_objects[1]
        environment = list_of_objects[2]
        exogeneous_agents = list_of_objects[3]
        funds = list_of_objects[4]




        fx.append(1/environment.var.fx_rates.iloc[0,1])
        d_ra1.append(funds[0].exp.returns[portfolios[1]])
        d_ra0.append(funds[0].exp.returns[portfolios[0]])

        f_ra1.append(funds[1].exp.returns[portfolios[1]])
        f_ra0.append(funds[1].exp.returns[portfolios[0]])


        d_q1.append(funds[0].var.assets[portfolios[1]])
        d_q0.append(funds[0].var.assets[portfolios[0]])
        f_q1.append(funds[1].var.assets[portfolios[1]])
        f_q0.append(funds[1].var.assets[portfolios[0]])

        d_c1.append(funds[0].var.currency[currencies[1]])
        d_c0.append(funds[0].var.currency[currencies[0]])
        f_c1.append(funds[1].var.currency[currencies[1]])
        f_c0.append(funds[1].var.currency[currencies[0]])


        d_rc1.append(funds[0].exp.returns[currencies[1]])
        d_rc0.append(funds[0].exp.returns[currencies[0]])

        f_rc1.append(funds[1].exp.returns[currencies[1]])
        f_rc0.append(funds[1].exp.returns[currencies[0]])

        hb_d.append(funds[0].var.weights[portfolios[1]] + funds[0].var.weights[currencies[1]])
        hb_f.append(funds[1].var.weights[portfolios[0]] + funds[1].var.weights[currencies[0]])

        d_dc.append(funds[0].var.weights[currencies[0]])
        d_fc.append(funds[0].var.weights[currencies[1]])
        d_da.append(funds[0].var.weights[portfolios[0]])
        d_fa.append(funds[0].var.weights[portfolios[1]])

        f_dc.append(funds[1].var.weights[currencies[0]])
        f_fc.append(funds[1].var.weights[currencies[1]])
        f_da.append(funds[1].var.weights[portfolios[0]])
        f_fa.append(funds[1].var.weights[portfolios[1]])

        cov_11.append(funds[0].var.covariance_matrix.loc[portfolios[1], portfolios[1]])
        cov_00.append(funds[0].var.covariance_matrix.loc[portfolios[0], portfolios[0]])
        cov_01.append(funds[0].var.covariance_matrix.loc[portfolios[0], portfolios[1]])

    fx_dict.update({obj_label: fx})

    d_ra0_dict.update({obj_label: d_ra0})
    d_ra1_dict.update({obj_label: d_ra1})

    f_ra0_dict.update({obj_label: f_ra0})
    f_ra1_dict.update({obj_label: f_ra1})

    cov_11_dict.update({obj_label: cov_11})
    cov_00_dict.update({obj_label: cov_00})
    cov_01_dict.update({obj_label: cov_01})

    d_q0_dict.update({obj_label: d_q0})
    d_q1_dict.update({obj_label: d_q1})
    f_q0_dict.update({obj_label: f_q0})
    f_q1_dict.update({obj_label: f_q1})

    d_c0_dict.update({obj_label: d_c0})
    d_c1_dict.update({obj_label: d_c1})
    f_c0_dict.update({obj_label: f_c0})
    f_c1_dict.update({obj_label: f_c1})


    d_rc0_dict.update({obj_label: d_rc0})
    d_rc1_dict.update({obj_label: d_rc1})

    f_rc0_dict.update({obj_label: f_rc0})
    f_rc1_dict.update({obj_label: f_rc1})

    hb_d_dict.update({obj_label: hb_d})
    hb_f_dict.update({obj_label: hb_f})

    d_dc_dict.update({obj_label: d_dc})
    d_fc_dict.update({obj_label: d_fc})
    d_da_dict.update({obj_label: d_da})
    d_fa_dict.update({obj_label: d_fa})

    f_dc_dict.update({obj_label: f_dc})
    f_fc_dict.update({obj_label: f_fc})
    f_da_dict.update({obj_label: f_da})
    f_fa_dict.update({obj_label: f_fa})


FX =np.empty((0,2), float)

D_R0_mean = np.empty((0, 2), float)
D_R0_std = np.empty((0, 2), float)

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


HB_D_mean =np.empty((0,2), float)
HB_F_mean =np.empty((0,2), float)
HB_D_5 =np.empty((0,2), float)
HB_F_5 =np.empty((0,2), float)
HB_D_95 =np.empty((0,2), float)
HB_F_95 =np.empty((0,2), float)

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

FX_mean =np.empty((0,2), float)
FX_5 =np.empty((0,2), float)
FX_95 =np.empty((0,2), float)



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

D_C0_mean =np.empty((0,2), float)
D_C1_mean =np.empty((0,2), float)
D_C0_5 =np.empty((0,2), float)
D_C1_5 =np.empty((0,2), float)
D_C0_95 =np.empty((0,2), float)
D_C1_95 =np.empty((0,2), float)
F_C0_mean=np.empty((0,2), float)
F_C1_mean=np.empty((0,2), float)
F_C0_5=np.empty((0,2), float)
F_C1_5=np.empty((0,2), float)
F_C0_95=np.empty((0,2), float)
F_C1_95=np.empty((0,2), float)

COV_00_mean=np.empty((0,2), float)
COV_11_mean=np.empty((0,2), float)
COV_01_mean=np.empty((0,2), float)

COV_00_5=np.empty((0,2), float)
COV_11_5=np.empty((0,2), float)
COV_01_5=np.empty((0,2), float)

COV_00_95=np.empty((0,2), float)
COV_11_95=np.empty((0,2), float)
COV_01_95=np.empty((0,2), float)



for i in sorted(fx_dict.iterkeys()):
    f=  np.array(fx_dict[i])

    f_diff = np.diff(f)
    f_p_diff = f_diff / f[:-1]

    d_ys_r0= np.array(d_ra0_dict[i]) - np.array(d_rc0_dict[i])
    d_ys_r1= np.array(d_ra1_dict[i]) - np.array(d_rc1_dict[i])

    f_ys_r0= np.array(f_ra0_dict[i]) - np.array(f_rc0_dict[i])
    f_ys_r1= np.array(f_ra1_dict[i]) - np.array(f_rc1_dict[i])

    FX=np.append(FX, np.array([[float(i.split("_")[-1]),np.std(f)]]),axis=0)
    FX_mean=np.append(FX_mean, np.array([[float(i.split("_")[-1]),np.mean(f)]]),axis=0)
    FX_5 = np.append(FX_5, np.array([[float(i.split("_")[-1]), np.percentile(f, 5)]]), axis=0)
    FX_95 = np.append(FX_95, np.array([[float(i.split("_")[-1]), np.percentile(f, 95)]]), axis=0)

    D_R0_std=np.append(D_R0_std, np.array([[float(i.split("_")[-1]), np.std(d_ys_r0)]]), axis=0)
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

    D_C0_mean=np.append(D_C0_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_c0_dict[i]))]]), axis=0)
    D_C1_mean=np.append(D_C1_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_c1_dict[i]))]]), axis=0)
    D_C0_5 = np.append(D_C0_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_c0_dict[i]), 5)]]), axis=0)
    D_C1_5 = np.append(D_C1_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_c1_dict[i]), 5)]]), axis=0)
    D_C0_95 = np.append(D_C0_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_c0_dict[i]), 95)]]), axis=0)
    D_C1_95 = np.append(D_C1_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_c1_dict[i]), 95)]]), axis=0)

    F_C0_mean=np.append(F_C0_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_c0_dict[i]))]]), axis=0)
    F_C1_mean=np.append(F_C1_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_c1_dict[i]))]]), axis=0)
    F_C0_5 = np.append(F_C0_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_c0_dict[i]), 5)]]), axis=0)
    F_C1_5 = np.append(F_C1_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_c1_dict[i]), 5)]]), axis=0)
    F_C0_95 = np.append(F_C0_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_c0_dict[i]), 95)]]), axis=0)
    F_C1_95 = np.append(F_C1_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_c1_dict[i]), 95)]]), axis=0)







    HB_D_mean = np.append(HB_D_mean, np.array([[float(i.split("_")[-1]),np.mean(np.array(hb_d_dict[i]))]]),axis=0)
    HB_F_mean = np.append(HB_F_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(hb_f_dict[i]))]]), axis=0)
    HB_D_5 = np.append(HB_D_5, np.array([[float(i.split("_")[-1]),np.percentile(np.array(hb_d_dict[i]),5)]]),axis=0)
    HB_F_5 = np.append(HB_F_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(hb_f_dict[i]),5)]]), axis=0)
    HB_D_95 = np.append(HB_D_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(hb_d_dict[i]),95)]]),axis=0)
    HB_F_95 = np.append(HB_F_95, np.array([[float(i.split("_")[-1]), np.percentile(np.array(hb_f_dict[i]),95)]]), axis=0)

    D_DC_mean = np.append(D_DC_mean, np.array([[float(i.split("_")[-1]),np.mean(np.array(d_dc_dict[i]))]]),axis=0)
    D_FC_mean = np.append(D_FC_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_fc_dict[i]))]]), axis=0)
    D_DA_mean = np.append(D_DA_mean, np.array([[float(i.split("_")[-1]),np.mean(np.array(d_da_dict[i]))]]),axis=0)
    D_FA_mean = np.append(D_FA_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(d_fa_dict[i]))]]), axis=0)

    D_DC_5 = np.append(D_DC_5, np.array([[float(i.split("_")[-1]),np.percentile(np.array(d_dc_dict[i]),5)]]),axis=0)
    D_FC_5 = np.append(D_FC_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_fc_dict[i]),5)]]), axis=0)
    D_DA_5 = np.append(D_DA_5, np.array([[float(i.split("_")[-1]),np.percentile(np.array(d_da_dict[i]),5)]]),axis=0)
    D_FA_5 = np.append(D_FA_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(d_fa_dict[i]),5)]]), axis=0)

    D_DC_95 = np.append(D_DC_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(d_dc_dict[i]),95)]]),axis=0)
    D_FC_95 = np.append(D_FC_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(d_fc_dict[i]),95)]]), axis=0)
    D_DA_95 = np.append(D_DA_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(d_da_dict[i]),95)]]),axis=0)
    D_FA_95 = np.append(D_FA_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(d_fa_dict[i]),95)]]), axis=0)

    F_DC_mean = np.append(F_DC_mean, np.array([[float(i.split("_")[-1]),np.mean(np.array(f_dc_dict[i]))]]),axis=0)
    F_FC_mean = np.append(F_FC_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_fc_dict[i]))]]), axis=0)
    F_DA_mean = np.append(F_DA_mean, np.array([[float(i.split("_")[-1]),np.mean(np.array(f_da_dict[i]))]]),axis=0)
    F_FA_mean = np.append(F_FA_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(f_fa_dict[i]))]]), axis=0)

    F_DC_5 = np.append(F_DC_5, np.array([[float(i.split("_")[-1]),np.percentile(np.array(f_dc_dict[i]),5)]]),axis=0)
    F_FC_5 = np.append(F_FC_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_fc_dict[i]),5)]]), axis=0)
    F_DA_5 = np.append(F_DA_5, np.array([[float(i.split("_")[-1]),np.percentile(np.array(f_da_dict[i]),5)]]),axis=0)
    F_FA_5 = np.append(F_FA_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(f_fa_dict[i]),5)]]), axis=0)

    F_DC_95 = np.append(F_DC_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(f_dc_dict[i]),95)]]),axis=0)
    F_FC_95 = np.append(F_FC_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(f_fc_dict[i]),95)]]), axis=0)
    F_DA_95 = np.append(F_DA_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(f_da_dict[i]),95)]]),axis=0)
    F_FA_95 = np.append(F_FA_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(f_fa_dict[i]),95)]]), axis=0)


    COV_00_mean = np.append(COV_00_mean, np.array([[float(i.split("_")[-1]),np.mean(np.array(cov_00_dict[i]))]]),axis=0)
    COV_11_mean = np.append(COV_11_mean, np.array([[float(i.split("_")[-1]), np.mean(np.array(cov_11_dict[i]))]]), axis=0)
    COV_01_mean = np.append(COV_01_mean, np.array([[float(i.split("_")[-1]),np.mean(np.array(cov_01_dict[i]))]]),axis=0)

    COV_00_5 = np.append(COV_00_5, np.array([[float(i.split("_")[-1]),np.percentile(np.array(cov_00_dict[i]),5)]]),axis=0)
    COV_11_5 = np.append(COV_11_5, np.array([[float(i.split("_")[-1]), np.percentile(np.array(cov_11_dict[i]),5)]]), axis=0)
    COV_01_5 = np.append(COV_01_5, np.array([[float(i.split("_")[-1]),np.percentile(np.array(cov_01_dict[i]),5)]]),axis=0)

    COV_00_95 = np.append(COV_00_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(cov_00_dict[i]),95)]]),axis=0)
    COV_11_95 = np.append(COV_11_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(cov_11_dict[i]),95)]]), axis=0)
    COV_01_95 = np.append(COV_01_95, np.array([[float(i.split("_")[-1]),np.percentile(np.array(cov_01_dict[i]),95)]]),axis=0)



rc('text', usetex=True)






fig, ax = plt.subplots()
x=D_FA_mean[:,0]
y=D_FA_mean[:,1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-b", label='a')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x[:], new_y[:],":r",label="s")

x=D_FA_5[:,0]
y=D_FA_5[:,1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label='b')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')


x=D_FA_95[:,0]
y=D_FA_95[:,1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,linestyle='--',color='xkcd:grey')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='lower center', frameon=False, labelspacing = 1.5)
plt.savefig('D_mat_foreign_asset.eps', format="eps")
plt.close()




fig, ax = plt.subplots()
x=D_DC_mean[:,0]
y=D_DC_mean[:,1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-b", label='a')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x[:], new_y[:],":r",label="s")

x=D_DC_5[:,0]
y=D_DC_5[:,1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label='b')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=D_DC_95[:,0]
y=D_DC_95[:,1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='lower center', frameon=False, labelspacing = 1.5)
plt.savefig('D_mat_domestic_cash.eps', format="eps")
plt.close()


fig, ax = plt.subplots()
x=D_FC_mean[:,0]
y=D_FC_mean[:,1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-b", label='a')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x[:], new_y[:],":r",label="s")

x=D_FC_5[:,0]
y=D_FC_5[:,1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label='b')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=D_FC_95[:,0]
y=D_FC_95[:,1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='upper left', frameon=False, labelspacing = 1.5)
plt.savefig('D_mat_foreign_cash.eps', format="eps")
plt.close()


fig, ax = plt.subplots()
x=D_DA_mean[:,0]
y=D_DA_mean[:,1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y,"-b", label='a')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x[:], new_y[:],":r",label="s")


x=D_DA_5[:,0]
y=D_DA_5[:,1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label='b')

new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x=D_DA_95[:,0]
y=D_DA_95[:,1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='upper center', frameon=False, labelspacing = 1.5)
plt.savefig('D_mat_domestic_asset.eps', format="eps")
plt.close()






fig, ax = plt.subplots()
x= D_R0_mean[:, 0]
y= D_R0_mean[:, 1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100*250)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x[:-1], new_y[:-1],"-b", label='a')

new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x[:], new_y[:],":r",label="s")


x= D_R0_5[:, 0]
y= D_R0_5[:, 1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100*250)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x= D_R0_95[:, 0]
y= D_R0_95[:, 1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100*250)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label='c')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='lower center', frameon=False, labelspacing = 1.5)
plt.savefig('D_mat_a0_excess_returns.eps', format="eps")
plt.close()







fig, ax = plt.subplots()
x= COV_00_mean[:, 0]
y= COV_00_mean[:, 1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x[:-1], new_y[:-1],"-b", label='a')

new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x[:], new_y[:],":r",label="s")


x= COV_00_5[:, 0]
y= COV_00_5[:, 1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x= COV_00_95[:, 0]
y= COV_00_95[:, 1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label='c')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')



x= COV_11_mean[:, 0]
y= COV_11_mean[:, 1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x[:-1], new_y[:-1],"-b", label='a')

new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x[:], new_y[:],":r",label="s")


x= COV_11_5[:, 0]
y= COV_11_5[:, 1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x= COV_11_95[:, 0]
y= COV_11_95[:, 1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label='c')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='lower center', frameon=False, labelspacing = 1.5)


x= COV_01_mean[:, 0]
y= COV_01_mean[:, 1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x[:-1], new_y[:-1],"-b", label='a')

new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x[:], new_y[:],":r",label="s")


x= COV_01_5[:, 0]
y= COV_01_5[:, 1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')

x= COV_01_95[:, 0]
y= COV_01_95[:, 1]
x = (np.array(x)-1)*(np.log(x)-1)/(np.log(x)**2)/250
y=np.multiply(y,100)
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey', label='c')
new_x=[0, new_x[-2]]
new_y = [new_y[-1]]*2
ax.plot(new_x, new_y, linestyle='--',color='xkcd:grey')
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='lower center', frameon=False, labelspacing = 1.5)

plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='lower center', frameon=False, labelspacing = 1.5)
plt.savefig('D_mat_covs.eps', format="eps")
plt.close()



from yield_curve_calc import *
from scipy.optimize import basinhopping
from scipy.optimize import minimize
from scipy.optimize import fsolve
from scipy.interpolate import interp1d

m = D_R0_mean[:-1, 0]
rm = D_R0_mean[:-1, 1]
t=1/(1-m)
t_asymptotic = 100000
m2=np.append(m,(t_asymptotic-1)/float(t_asymptotic))
rm2 = np.append(rm,D_R0_mean[-1, 1])
m2=np.append(m2,0)
rm2 = np.append(rm2,0)

t2=1/(1-m2)
f = interp1d(t2, rm2)
f2 = interp1d(t2, rm2, kind='cubic')

t_new = np.linspace(np.min(t2), np.max(t2), num=t_asymptotic, endpoint=True)
rm_new=f(t_new)
m_new=(t_new-1)/t_new



# counterfactual: computes the model yield curve when assuming that the underlying yield curve is the model yield curve
test_rm = []
for M in m:
    test_rm.append(sum((1-M)*M**(t_new[j]-1)*rm_new[j] for j in range(len(rm_new))))


starting_values = [0.05/250,-0.05/250,0,500]
beta0 = D_R0_mean[-1, 1]  # a in the mathematica file
f2 = interp1d(t, rm, kind='cubic')
t_opt = np.linspace(np.min(t), np.max(t), num=1000, endpoint=True)
rm_opt=f2(t_opt)
m_opt = (t_opt-1)/t_opt
#m_opt=np.append(m_opt,(t_asymptotic-1)/float(t_asymptotic))
#rm_opt=np.append(rm_opt,D_R0_mean[-1, 1])

minimum_NandS= minimize(opt_fun_spot, starting_values, args=(m_opt,rm_opt), method='nelder-mead')


starting_values = [0.05/250,-0.05/250,0,0,2300,1000]
minimum_Sv= minimize(opt_fun_spot, starting_values, args=(m_opt,rm_opt), method='nelder-mead')










# computes the model yield curve assuming that the underlying yield curve is the estimated one (result of the minimize)
T=1/(1-np.max(m))
rt_NandS =ycm2rt(minimum_NandS.x, int(T))
rt_Sv =ycm2rt(minimum_Sv.x, int(T))







f2 = interp1d(t, rm, kind='cubic')
t_er = np.linspace(np.min(t), np.max(t), num=200, endpoint=True)
rm_er=f2(t_er)
m_er=(t_er-1)/t_er

rm_NandS=rt2rm(minimum_NandS.x, m_er)
rm_Sv=rt2rm(minimum_Sv.x, m_er)





fig, ax = plt.subplots()
ax.plot(np.array(range(len(rt_NandS)))/float(250),np.array(rt_NandS)*25000,"-r", label='c')
ax.plot(np.array(range(len(rt_Sv)))/float(250),np.array(rt_Sv)*25000,"-g", label='b')
ax.plot(np.array(t_er)/float(250),np.array(rm_er)*25000,"-b", label='a')
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='lower center', frameon=False, labelspacing = 1.5)
plt.savefig('yield_curves.eps', format="eps")

fig, ax = plt.subplots()
ax.axhline(y=0,  color='b', linestyle='-', label="a")
ax.plot(np.array(t_er)/float(250),np.array(rm_NandS)*25000-np.array(rm_er)*25000,"-r", label='c')
ax.plot(np.array(t_er)/float(250),np.array(rm_Sv)*25000-np.array(rm_er)*25000,"-g", label='b')
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='upper center', frameon=False, labelspacing = 1.5)
plt.savefig('yc_fit.eps', format="eps")




rm_ecb=[]
rt_ecb=[]
ecb_params=[0.536426, -0.526426, 23.565854, -21.686654, 7.219323, 5.975699]
ecb_params[0:4]=np.array(ecb_params[0:4])/25000
ecb_params[4:6]=np.array(ecb_params[4:6])*250
rm_ecb=rt2rm(ecb_params, m_er)
rt_ecb =ycm2rt(ecb_params, int(T))


fig, ax = plt.subplots()
ax.plot(np.array(range(len(rt_ecb)))/float(250),np.array(rt_ecb)*25000,"-b", label='a')
ax.plot(t_er/float(250),np.array(rm_ecb)*25000,"-r", label='b')
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='lower center', frameon=False, labelspacing = 1.5)
plt.savefig('ecb_yield_curves.eps', format="eps")


from datetime import datetime
from matplotlib.dates import date2num

data=pd.read_excel("yield_curve_data_allBonds.xls")
rm_09993 = []
rm_099 = []
dates=[]
for i in range(len(data)):
    params=[data["beta0"][i],data["beta1"][i],data["beta2"][i],data["beta3"][i],data["tau1"][i],data["tau2"][i]]
    params[0:4] = np.array(params[0:4]) / 25000
    params[4:6] = np.array(params[4:6]) * 250
    rm_09993.append(rt2rm(params, [0.9993]))
    rm_099.append(rt2rm(params, [0.99]))

    datetime_object = datetime.strptime(data["date"][i], '%d.%m.%Y')
    dates.append(date2num(datetime_object))
fig, ax = plt.subplots()
ax.plot_date(dates, np.array(rm_09993)*25000,fmt='b-', label='a')
ax.plot_date(dates, np.array(rm_099)*25000,fmt='r-', label='b')
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='upper center', frameon=False, labelspacing = 1.5)
plt.savefig('ecb_implied_portfolio_TS.eps', format="eps")