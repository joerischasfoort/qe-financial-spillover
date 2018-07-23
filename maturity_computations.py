import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.optimize import basinhopping


Fed_BS_data = {"0-15": 1133 + 249412}
Fed_BS_data.update({"16-90": 93310})
Fed_BS_data.update({"91-365": 307881})
Fed_BS_data.update({"366-1825": 1042558})
Fed_BS_data.update({"1826-3650": 296037+41885})
Fed_BS_data.update({"3651-5475": (619586+1679242)/2}) #assuming that 50% matures between 10 and 15 years and
Fed_BS_data.update({"5476 - 14240": (619586+1679242)/2}) # 50% matures between 15 and 40 years (this is very adhoc)
#Fed_BS_data.update({"7301-15000": 0})

data = Fed_BS_data

def plot_mat_structure(data):

    maturing_assets = {}
    day = []
    mat = []
    for bin in data:
        start_day = int(bin.split("-")[0])
        end_day = int(bin.split("-")[-1])
        t= start_day
        while t <= end_day:
            maturing_assets.update({t:data[bin]/(1+end_day-start_day)})
            t=t+1

    for i in sorted(maturing_assets.iterkeys()):
        day = np.append(day,i)
        mat = np.append(mat, maturing_assets[i])

    y = np.array(mat)/sum(np.array(mat))
    print(sum(np.multiply(np.array(day), y))/365)
    y=np.cumsum(y)
    y = 1-y
    plt.plot(day/365,y)



    num_assets = 2
    b = (0.0,1.0)
    bnds = [b for i in range(2*num_assets)]
    const= [{"type": "eq", "fun": cons}]
    minimizer_kwargs = { "args": (day,y), 'bounds':bnds, 'constraints': const}
    starting_values = [0 for i in range(2*num_assets-1)]
    starting_values.append(1)
    minimum = basinhopping(opt_fun,starting_values,stepsize = 0.01, minimizer_kwargs=minimizer_kwargs, niter_success=100)



    mat_aux = {}
    for var in range(len(minimum.x)/2):
        mat_aux.update({var: np.multiply(minimum.x[var] ** day, minimum.x[(len(minimum.x)/2)+var])})    
    mat =  sum(mat_aux[i] for i in mat_aux)
    
    plt.plot(day/365,mat)


def opt_fun(m, day,y):
    mat_aux = {}
    for var in range(len(m)/2):
        mat_aux.update({var: np.multiply(m[var] ** day, m[(len(m)/2)+var])})    
    mat =  sum(mat_aux[i] for i in mat_aux)
    return sum((y-mat)**2)

def cons(m):
    sum_weights = 1
    for i in range(len(m)/2):
        sum_weights = sum_weights - m[(len(m)/2)+i]
    return sum_weights
    

def  compute_average_mat(m):
    return ((m-1)*(np.log(m)-1)/(np.log(m)**2))/365    



