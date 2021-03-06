import  pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools



local_dir = "Objects_CB/"

bounds = [0.1,0.09,0.07,0.05,0.03,0.009,0.007,0.005,0.003,0.01,0.001,0.0001]#,0.00001,0.000001,0.0000001,0.00000001]

tau_dict = {}
fx_dict = {}
p0_dict = {}
p1_dict = {}



for i in bounds:
    obj_label =  str(i)


    #variables to extract
    tau = []
    fx = []
    p1 = []
    p0 = []


    for day in range(100,201):
        filename = local_dir + "objects_day_" + str(day) + "_seed_1_"  + obj_label+".pkl"
        data = open(filename,"rb")
        list_of_objects = pickle.load(data)

        portfolios = list_of_objects[0]
        currencies = list_of_objects[1]
        environment = list_of_objects[2]
        exogeneous_agents = list_of_objects[3]
        funds = list_of_objects[4]


        tau.append(environment.var.tau)

        fx.append(1/environment.var.fx_rates.iloc[0,1])

        p1.append(portfolios[1].var.price)
        p0.append(portfolios[0].var.price)


    tau_dict.update({obj_label: tau})
    fx_dict.update({obj_label: fx})
    p0_dict.update({obj_label: p0})
    p1_dict.update({obj_label: p1})

Tau=np.empty((0,2), float)
FX =np.empty((0,2), float)
P0=np.empty((0,2), float)
P1 =np.empty((0,2), float)

for i in tau_dict:
    Tau=np.append(Tau, np.array([[float(i),sum(tau_dict[i])/float(101)]]),axis=0)


rc('text', usetex=True)

# two axis plot of average tau and fx inefficiency
x=Tau[:,0]
y=Tau[:,1]
lists = sorted(itertools.izip(*[x, y]))
new_x, new_y = list(itertools.izip(*lists))
fig, ax = plt.subplots()
ax.semilogx(new_x, new_y)
plt.xlabel("x")
plt.ylabel('y')
plt.savefig('efficiency_trade_off.eps', format="eps")
plt.close()





# two line plot of price inefficiency
#fig, ax = plt.subplots()
#x=P0[:,0]
#y=P0[:,1]
#y=np.multiply(y,100)
#lists = sorted(itertools.izip(*[x, y]))
#new_x, new_y = list(itertools.izip(*lists))
#ax.semilogx(new_x, new_y, '-b', label='a')

#x=P1[:,0]
#y=P1[:,1]
#y=np.multiply(y,100)
#lists = sorted(itertools.izip(*[x, y]))
#new_x, new_y = list(itertools.izip(*lists))
#ax.semilogx(new_x, new_y, '--r', label='b')
#LEGEND = ax.legend(loc='upper left', frameon=False, labelspacing=1.5)
#plt.xlabel(r'x')
#plt.ylabel(r'y')
#plt.savefig('Price_inefficiency.eps', format="eps")
#plt.close()

