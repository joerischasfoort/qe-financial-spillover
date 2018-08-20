import  pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools
from matplotlib.ticker import ScalarFormatter


local_dir = "Objects_MAT_negint/"

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















