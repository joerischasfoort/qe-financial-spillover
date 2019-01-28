import  pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools
from analysis_functions import *
from yield_curve_functions import *
from scipy.optimize import basinhopping
from scipy.optimize import minimize
from scipy.optimize import fsolve
from scipy.interpolate import interp1d

start_day = 2
end_day = 1000

variable =  [0.08,0.5,1,2,4,6.25,8,10,12,14,16,18,20,30,40]
experiments = ["MATwQE_med_", "MAT_med_"]
seed = 1






for e in experiments:
    filename = 'raw_and_relative_data_'+str(e)+'seed_' + str(seed) + '.pkl'
    data = open(filename, "rb")
    list_of_objects = pickle.load(data)
    seedx = list_of_objects[0]
    locals()[e+'raw_data'] = list_of_objects[1]
    relative_data = list_of_objects[2]

    var = "funds[0].exp.returns[portfolios[0]]"
    locals()[e+'os'] = [e+str(i) for i in variable]
    locals()[e+'rm'] = np.array([np.mean(locals()[e+'raw_data'][o][var][:]) for o in locals()[e+'os']])
    m = (np.array(variable) * 250 - 1) / (np.array(variable) * 250)
    t = np.array(variable)*250

    f2 = interp1d(t, locals()[e+'rm'])
    #f2 = interp1d(t, locals()[e+'rm'], kind='cubic')

    t_opt = np.linspace(np.min(t), np.max(t), num=100, endpoint=True)
    rm_opt = f2(t_opt)
    m_opt = (t_opt - 1) / t_opt

    starting_values = [0.03 / 250, -0.045 / 250, 0.4/250, -0.35/250, 3300, 2700]
    minimum_Sv = minimize(opt_fun_spot, starting_values, args=(m_opt, rm_opt), method='nelder-mead')

    print(minimum_Sv)
    locals()[e+'x']=minimum_Sv.x
    T = 1 / (1 - np.max(m))
    locals()[e + 'rt_Sv'] = ycm2rt(minimum_Sv.x, int(T))
    #rt_Sv

    t_er = np.linspace(np.min(t), np.max(t), num=100, endpoint=True)
    locals()[e + 'rm_er'] = f2(t_er)
    m_er = (t_er - 1) / t_er

    locals()[e + 'rm_Sv'] = rt2rm(minimum_Sv.x, m_er)


    fig, ax = plt.subplots()
    ax.plot(np.array(range(len(locals()[e + 'rt_Sv'])))/float(250),np.array(locals()[e + 'rt_Sv'])*25000,"-g", label='b')
    ax.plot(np.array(t_er)/float(250),np.array(locals()[e + 'rm_er'])*25000,"-b", label='a')
    plt.xlabel("x")
    plt.ylabel('y')
    ax.legend(loc='lower center', frameon=False, labelspacing = 1.5)
    plt.savefig(e+'yield_curves.eps', format="eps")



    fig, ax = plt.subplots()
    ax.axhline(y=0,  color='b', linestyle='-', label="a")
    ax.plot(np.array(t_er)/float(250),np.array(locals()[e + 'rm_Sv'])*25000-np.array(locals()[e + 'rm_er'])*25000,"-g", label='b')
    plt.xlabel("x")
    plt.ylabel('y')
    ax.legend(loc='upper center', frameon=False, labelspacing = 1.5)
    plt.savefig(e+'yc_fit.eps', format="eps")



data_mean, data_p5, data_p95 = compute_averages(MAT_med_raw_data, "MAT_med_6.25", MAT_med_os, range(0, 999))

var = 'funds[0].exp.returns[portfolios[0]]'
x_factor = 1
y_factor = 250*100
#y_factor = 1
location = 'upper left'
name = 'yield_curve_MAT'
saving = 1
plot_conf(var,data_mean, data_p5, data_p95, variable,x_factor,y_factor, location, name, saving)

data_mean_wQE, data_p5_wQE, data_p95_wQE = compute_averages(MATwQE_med_raw_data, "MATwQE_med_6.25", MATwQE_med_os, range(0, 999))

var = 'funds[0].exp.returns[portfolios[0]]'
x_factor = 1
y_factor = 250*100
#y_factor = 1
location = 'upper left'
name = 'yield_curve_MATwQE'
saving = 1
plot_conf(var,data_mean_wQE, data_p5_wQE, data_p95_wQE, variable,x_factor,y_factor, location, name, saving)


delta_data_mean = np.array(data_mean_wQE[var])-np.array(data_mean[var])


