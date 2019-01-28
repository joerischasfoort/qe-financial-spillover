

from yield_curve_functions import *
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
rm_099936 = []
rm_099 = []
dates=[]
for i in range(len(data)):
    params=[data["beta0"][i],data["beta1"][i],data["beta2"][i],data["beta3"][i],data["tau1"][i],data["tau2"][i]]
    params[0:4] = np.array(params[0:4]) / 25000
    params[4:6] = np.array(params[4:6]) * 250
    rm_09993.append(rt2rm(params, [0.99936]))
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