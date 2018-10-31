import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.optimize import basinhopping
import pandas as pd
import os
print os.getcwd()

Fed_BS_data = {"0-15": 1133 + 249412}
Fed_BS_data.update({"16-90": 93310})
Fed_BS_data.update({"91-365": 307881})
Fed_BS_data.update({"366-1825": 1042558})
Fed_BS_data.update({"1826-3650": 296037+41885})
Fed_BS_data.update({"3651-5475": (619586+1679242)/2}) #assuming that 50% matures between 10 and 15 years and
Fed_BS_data.update({"5476 - 14240": (619586+1679242)/2}) # 50% matures between 15 and 40 years (this is very adhoc)
#Fed_BS_data.update({"7301-15000": 0})


US_fund_data = {"0-365": 2}
US_fund_data.update({"366-1095": 6})
US_fund_data.update({"1096-1825": 7})
US_fund_data.update({"1826-2555": 5})
US_fund_data.update({"2556-3650": 8})
US_fund_data.update({"3651-5475": 2}) #assuming that 50% matures between 10 and 15 years and
US_fund_data.update({"5476-7300": 2}) # 50% matures between 15 and 40 years (this is very adhoc)
US_fund_data.update({"7301-10950": 6})
US_fund_data.update({"10951-14210": 1})
#


df = pd.read_excel("funds/old_small_samples_before_automating_MSdownload/MS_360euro_baseCUR.xlsx")



data = Fed_BS_data

def plot_mat_structure(data):

    days_in_year = 250

    maturing_assets = {}
    day = []
    mat = []
    for bin in data:
        start_day = int(bin.split("-")[0])
        end_day = int(bin.split("-")[-1])

        start_day = (start_day/float(365))*days_in_year
        end_day = (end_day/float(365))*days_in_year

        t= start_day
        while t <= end_day:
            maturing_assets.update({t:data[bin]/float((1+end_day-start_day))})
            t=t+1

    for i in sorted(maturing_assets.iterkeys()):
        day = np.append(day,i)
        mat = np.append(mat, maturing_assets[i])

    y = np.array(mat)/sum(np.array(mat))
    print(sum(np.multiply(np.array(day), y))/days_in_year)
    y=np.cumsum(y)
    y = 1-y
    plt.plot(day/days_in_year,y)



    num_assets = 2
    b = (0.0,1.0)
    bnds = [b for i in range(2*num_assets)]
    const= [{"type": "eq", "fun": cons}]
    minimizer_kwargs = { "args": (day,y), 'bounds':bnds, 'constraints': const}
    starting_values = [0 for i in range(2*num_assets-1)]
    starting_values.append(1)
    minimum = basinhopping(opt_fun,starting_values,stepsize = 0.01, minimizer_kwargs=minimizer_kwargs, niter_success=1000)



    mat_aux = {}
    for var in range(len(minimum.x)/2):
        mat_aux.update({var: np.multiply(minimum.x[var] ** day, minimum.x[(len(minimum.x)/2)+var])})    
    mat =  sum(mat_aux[i] for i in mat_aux)
    
    plt.plot(day/days_in_year,mat)


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
    

def  compute_average_mat(m,days_in_year):
    return ((m-1)*(np.log(m)-1)/(np.log(m)**2))/days_in_year



