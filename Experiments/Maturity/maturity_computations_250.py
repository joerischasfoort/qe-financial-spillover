import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.optimize import basinhopping
import pandas as pd
import os
print os.getcwd()
from matplotlib import rc



EZ = pd.read_excel("C:/Users/jrr/Dropbox/International Spillovers/Data/funds_and_banks/downloaded data/EZ15000_nolinks.xlsx")




import math


FI_eme_total, EQ_eme_total = 0, 0
total_assets = 0
mat_1, mat_3, mat_5, mat_7, mat_10, mat_15, mat_20, mat_30 = 0,0,0,0,0,0,0,0
cash_weight, eq_weight, bond_weight = 0,0,0


EZ['Fund_Size_Estimated_Monthly'] = pd.to_numeric(EZ['Fund_Size_Estimated_Monthly'], errors='coerce')
EZ['Maturity_1-3Yr'] = pd.to_numeric(EZ['Maturity_1-3Yr'], errors='coerce')
EZ['Maturity_3-5Yr'] = pd.to_numeric(EZ['Maturity_3-5Yr'], errors='coerce')
EZ['Maturity_5-7Yr'] = pd.to_numeric(EZ['Maturity_5-7Yr'], errors='coerce')
EZ['Maturity_7-10Yr'] = pd.to_numeric(EZ['Maturity_7-10Yr'],errors='coerce')
EZ['Maturity_10-15Yr'] = pd.to_numeric(EZ['Maturity_10-15Yr'], errors='coerce')
EZ['Maturity_15-20Yr'] = pd.to_numeric(EZ['Maturity_15-20Yr'],errors='coerce')
EZ['Maturity_20-30Yr'] = pd.to_numeric(EZ['Maturity_20-30Yr'],errors='coerce')
EZ['Maturity_30+Yr']= pd.to_numeric(EZ['Maturity_30+Yr'],errors='coerce')
EZ['Asset_Alloc_Cash'] = pd.to_numeric(EZ['Asset_Alloc_Cash'], errors='coerce')
EZ['Asset_Alloc_Bond'] = pd.to_numeric(EZ['Asset_Alloc_Bond'], errors='coerce')
EZ['Asset_Alloc_Equity'] = pd.to_numeric(EZ['Asset_Alloc_Equity'], errors='coerce')
EZ['Cash'] = pd.to_numeric(EZ['Cash'], errors='coerce')
EZ['Currency_including_derivatives'] = pd.to_numeric(EZ['Currency_including_derivatives'], errors='coerce')


Bonds=(EZ['Asset_Alloc_Bond']/100)*EZ['Fund_Size_Estimated_Monthly']
Equities=(EZ['Asset_Alloc_Equity']/100)*EZ['Fund_Size_Estimated_Monthly']
DomesticCash=(EZ['Asset_Alloc_Cash']/100)*EZ['Fund_Size_Estimated_Monthly']*(EZ['Cash']/100)
ForeignCash=(EZ['Asset_Alloc_Cash']/100)*EZ['Fund_Size_Estimated_Monthly']*(EZ['Currency_including_derivatives']/100)
STassets=(EZ['Asset_Alloc_Cash']/100)*EZ['Fund_Size_Estimated_Monthly']-DomesticCash-ForeignCash


mat_0=(STassets)
mat_1=(EZ['Fund_Size_Estimated_Monthly']*(EZ['Maturity_1-3Yr']/100)*EZ['Asset_Alloc_Bond']/100)
mat_3=(EZ['Fund_Size_Estimated_Monthly']*(EZ['Maturity_3-5Yr']/100)*EZ['Asset_Alloc_Bond']/100)
mat_5=(EZ['Fund_Size_Estimated_Monthly']*(EZ['Maturity_5-7Yr']/100)*EZ['Asset_Alloc_Bond']/100)
mat_7=(EZ['Fund_Size_Estimated_Monthly']*(EZ['Maturity_7-10Yr']/100)*EZ['Asset_Alloc_Bond']/100)
mat_10=(EZ['Fund_Size_Estimated_Monthly']*(EZ['Maturity_10-15Yr']/100)*EZ['Asset_Alloc_Bond']/100)
mat_15=(EZ['Fund_Size_Estimated_Monthly']*(EZ['Maturity_15-20Yr']/100)*EZ['Asset_Alloc_Bond']/100)
mat_20=(EZ['Fund_Size_Estimated_Monthly']*(EZ['Maturity_20-30Yr']/100)*EZ['Asset_Alloc_Bond']/100)
mat_30=(EZ['Fund_Size_Estimated_Monthly']*(EZ['Maturity_30+Yr']/100)*EZ['Asset_Alloc_Bond']/100)

total_FI=np.nansum(mat_0+mat_1+mat_3+mat_5+mat_7+mat_10+mat_15+mat_20+mat_30)
mat_0= np.nansum(mat_0)/total_FI
mat_1= np.nansum(mat_1)/total_FI
mat_3= np.nansum(mat_3)/total_FI
mat_5= np.nansum(mat_5)/total_FI
mat_7= np.nansum(mat_7)/total_FI
mat_10=np.nansum(mat_10)/total_FI
mat_15=np.nansum(mat_15)/total_FI
mat_20=np.nansum(mat_20)/total_FI
mat_30=np.nansum(mat_30)/total_FI

Fund_BS_data = {"0-365":  mat_0  } # <1 year
Fund_BS_data.update({"366-1095": mat_1})#1to3Yr
Fund_BS_data.update({"1096-1825": mat_3})#3to5Yr
Fund_BS_data.update({"1826-2555": mat_5})#5to7Yr
Fund_BS_data.update({"2556- 3650":  mat_7})#7to10Yr
Fund_BS_data.update({"3651-5475": mat_10 })#10to15Yr
Fund_BS_data.update({"5476-7300":  mat_15 })#15to20Yr
Fund_BS_data.update({"7301-10950": mat_20  }) #20to30Yr
Fund_BS_data.update({"10951 - 14600": mat_30}) # 30+
#Fund_BS_data.update({"7301-15000": 0})

data = Fund_BS_data
print data


def plot_mat_structure(data):

    days_in_year = 250

    maturing_assets = {}
    day = []
    mat = []
    for bin in data:
        start_day = int(bin.split("-")[0])
        end_day = int(bin.split("-")[-1])

        start_day = math.ceil((start_day/float(365))*days_in_year)
        end_day = math.floor((end_day/float(365))*days_in_year)

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
    rc('text', usetex=True)
    fig, ax = plt.subplots()
    ax.plot(day/days_in_year,y*100,'-b',label='a')



    num_assets = 1
    b = (0.0,1.0)
    bnds = [b for i in range(2*num_assets)]
    const= [{"type": "eq", "fun": cons}]
    minimizer_kwargs = { "args": (day,y), 'bounds':bnds, 'constraints': const}
    starting_values = [0 for i in range(2*num_assets-1)]
    starting_values.append(1)
    minimum = basinhopping(opt_fun,starting_values,stepsize = 0.01, minimizer_kwargs=minimizer_kwargs, niter_success=1000)

    print minimum.x

    mat_aux = {}
    for var in range(len(minimum.x)/2):
        mat_aux.update({var: np.multiply(minimum.x[var] ** day, minimum.x[(len(minimum.x)/2)+var])})
    mat =  sum(mat_aux[i] for i in mat_aux)

    ax.plot(day/days_in_year,mat*100,'-r',label='b')
    plt.xlabel("x")
    plt.ylabel('y')
    ax.legend(loc='upper center', frameon=False, labelspacing=1.5)
    plt.savefig('maturity_structure_funds.eps', format="eps")

    return minimum

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

min = plot_mat_structure(data)