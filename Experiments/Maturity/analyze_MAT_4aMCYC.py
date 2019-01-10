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
    filename = e+'MC_means.pkl'
    data = open(filename, "rb")
    list_of_objects = pickle.load(data)
    locals()[e + 'MC_mean_raw'] = list_of_objects[0]
    locals()[e+'MC_p5_raw'] = list_of_objects[1]
    locals()[e + 'MC_p95_raw'] = list_of_objects[2]

    ordered_var_list = []
    for i in variable:
        obj_label = e + str(i)
        ordered_var_list.append(obj_label)

    locals()[e + 'MC_mean'] = []
    locals()[e + 'MC_p5'] = []
    locals()[e + 'MC_p95'] = []

    for o in ordered_var_list:
        locals()[e + 'MC_mean'].append(locals()[e + 'MC_mean_raw'][o])
        locals()[e + 'MC_p5'].append(locals()[e+'MC_p5_raw'][o])
        locals()[e + 'MC_p95'].append(locals()[e+'MC_p95_raw'][o])


    m = (np.array(variable) * 250 - 1) / (np.array(variable) * 250)
    t = np.array(variable)*250

    f2 = interp1d(t, locals()[e+'MC_mean'])
    f2p5 = interp1d(t, locals()[e+'MC_p5'])
    f2p95 = interp1d(t, locals()[e+'MC_p95'])

    #f2 = interp1d(t, locals()[e+'MC_mean'], kind='cubic')

    t_opt = np.linspace(np.min(t), np.max(t), num=100, endpoint=True)
    rm_opt = f2(t_opt)

    t_opt = t
    rm_opt = locals()[e+'MC_mean']
    rm_opt_p5 = locals()[e+'MC_p5']
    rm_opt_p95 = locals()[e+'MC_p95']

    m_opt = (t_opt - 1) / t_opt

    starting_values = [0.03 / 250, -0.045 / 250, 0.4/250, -0.35/250, 3300, 2700]
    minimum_Sv = minimize(opt_fun_spot, starting_values, args=(m_opt, rm_opt), method='nelder-mead')
    minimum_Sv_p5 = minimize(opt_fun_spot, starting_values, args=(m_opt, rm_opt_p5), method='nelder-mead')
    minimum_Sv_p95 = minimize(opt_fun_spot, starting_values, args=(m_opt, rm_opt_p95), method='nelder-mead')

    #print(minimum_Sv)
    locals()[e+'x']=minimum_Sv.x

    T = 1 / (1 - np.max(m))
    locals()[e + 'rt_Sv'] = ycm2rt(minimum_Sv.x, int(T))
    locals()[e + 'rt_Sv_p5'] = ycm2rt(minimum_Sv_p5.x, int(T))
    locals()[e + 'rt_Sv_p95'] = ycm2rt(minimum_Sv_p95.x, int(T))

    #rt_Sv

    #t_er = np.linspace(np.min(t), np.max(t), num=100, endpoint=True)
    #locals()[e + 'rm_er'] = f2(t_er)
    #m_er = (t_er - 1) / t_er

    t_er = t
    locals()[e + 'rm_er'] = rm_opt
    locals()[e + 'rm_er_p5'] = rm_opt_p5
    locals()[e + 'rm_er_p95'] = rm_opt_p95

    m_er = (t_er - 1) / t_er



    locals()[e + 'rm_Sv'] = rt2rm(minimum_Sv.x, m_er)
    locals()[e + 'rm_Sv_p5'] = rt2rm(minimum_Sv_p5.x, m_er)
    locals()[e + 'rm_Sv_p95'] = rt2rm(minimum_Sv_p95.x, m_er)





    fig, ax = plt.subplots()
    ax.axhline(y=0,  color='b', linestyle='-', label="a")
    ax.plot(np.array(t_er)/float(250),np.array(locals()[e + 'rm_Sv'])*25000-np.array(locals()[e + 'rm_er'])*25000,"-g", label='b')
    plt.xlabel("x")
    plt.ylabel('y')
    ax.legend(loc='upper center', frameon=False, labelspacing = 1.5)
    plt.savefig(e+'yc_fit.eps', format="eps")

    fig, ax = plt.subplots()
    ax.axhline(y=0,  color='b', linestyle='-', label="a")
    ax.plot(np.array(t_er)/float(250),np.array(locals()[e + 'rm_Sv_p5'])*25000-np.array(locals()[e + 'rm_er_p5'])*25000,"-g", label='b')
    plt.xlabel("x")
    plt.ylabel('y')
    ax.legend(loc='upper center', frameon=False, labelspacing = 1.5)
    plt.savefig(e+'yc_fit_p5.eps', format="eps")


    fig, ax = plt.subplots()
    ax.axhline(y=0,  color='b', linestyle='-', label="a")
    ax.plot(np.array(t_er)/float(250),np.array(locals()[e + 'rm_Sv_p95'])*25000-np.array(locals()[e + 'rm_er_p95'])*25000,"-g", label='b')
    plt.xlabel("x")
    plt.ylabel('y')
    ax.legend(loc='upper center', frameon=False, labelspacing = 1.5)
    plt.savefig(e+'yc_fit_p95.eps', format="eps")


fig, ax = plt.subplots()
ax.plot(t/250,np.array(MAT_med_rm_er)*25000,"-b", label='a')
ax.plot(t/250,np.array(MAT_med_rm_er_p5)*25000,linestyle='--', color='xkcd:grey')
ax.plot(t/250,np.array(MAT_med_rm_er_p95)*25000,linestyle='--', color='xkcd:grey', label = "c")
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='upper left', frameon=False, labelspacing = 1.5)
plt.savefig('MAT_RM_yield_curves.eps', format="eps")




fig, ax = plt.subplots()
ax.plot(np.array(range(len(MAT_med_rt_Sv)))/float(250),np.array(MAT_med_rt_Sv)*25000,"-b", label='a')
ax.plot(np.array(range(len(MAT_med_rt_Sv_p5)))/float(250),np.array(MAT_med_rt_Sv_p5)*25000,linestyle='--', color='xkcd:grey')
ax.plot(np.array(range(len(MAT_med_rt_Sv_p95)))/float(250),np.array(MAT_med_rt_Sv_p95)*25000,linestyle='--', color='xkcd:grey', label = "c")
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='upper left', frameon=False, labelspacing = 1.5)
plt.savefig('MAT_yield_curves.eps', format="eps")

#fig, ax = plt.subplots()
#ax.plot(np.array(range(len(MATwQE_med_rt_Sv)))/float(250),np.array(MATwQE_med_rt_Sv)*25000,"-b", label='a')
#ax.plot(np.array(range(len(MATwQE_med_rt_Sv_p5)))/float(250),np.array(MATwQE_med_rt_Sv_p5)*25000,linestyle='--', color='xkcd:grey')
#ax.plot(np.array(range(len(MATwQE_med_rt_Sv_p95)))/float(250),np.array(MATwQE_med_rt_Sv_p95)*25000,linestyle='--', color='xkcd:grey', label = "c")
#plt.xlabel("x")
#plt.ylabel('y')
#ax.legend(loc='upper left', frameon=False, labelspacing = 1.5)
#plt.savefig('MATwQE_yield_curves.eps', format="eps")



fig, ax = plt.subplots()
ax.plot(np.array(range(len(MATwQE_med_rt_Sv)))/float(250),np.array(MATwQE_med_rt_Sv)*2500000-np.array(MAT_med_rt_Sv)*2500000,"-b", label='a')
ax.plot(np.array(range(len(MATwQE_med_rt_Sv)))/float(250),np.array(MATwQE_med_rt_Sv_p5)*2500000-np.array(MAT_med_rt_Sv_p5)*2500000,linestyle='--', color='xkcd:grey')
ax.plot(np.array(range(len(MATwQE_med_rt_Sv)))/float(250),np.array(MATwQE_med_rt_Sv_p95)*2500000-np.array(MAT_med_rt_Sv_p95)*2500000,linestyle='--', color='xkcd:grey', label = "c")
plt.xlabel("x")
plt.ylabel('y')
ax.legend(loc='lower left', frameon=False, labelspacing = 1.5)
plt.savefig('yield_effects.eps', format="eps")


fig, ax = plt.subplots()
ax.plot(np.array(range(len(MATwQE_med_rt_Sv)))/float(250),np.array(MATwQE_med_rt_Sv)*2500000-np.array(MAT_med_rt_Sv)*2500000,"-b")
plt.xlabel("x")
plt.ylabel('y')
plt.savefig('mean_yield_effects.eps', format="eps")
