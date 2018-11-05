import numpy as np
import matplotlib.pyplot as plt





def opt_fun_spot(y, m,rm):
    # see mathematica file: yield_curve_model_fit
    x=y[2:]
    beta0=y[0]
    beta1 = y[1]
    #beta1 = 0 - beta0

    sol_int = []
    aux_2 = np.zeros(len(x) / 2)
    for i in range(len(m)):
        aux_0 = beta0
        d = x[(len(x) / 2)]
        aux_1 = ((m[i]-1)*beta1*d*(np.log(1-m[i])-np.log(1-np.exp(-1/d)*m[i])))/m[i] #(b d (-1 + m) (Log[1 - m] - Log[1 - E^(-1/d) m]))/m
        for j, val in enumerate(aux_2):
            d = x[(len(x) / 2) + j]
            aux_2[j] =(m[i]-1)*x[j]/(np.exp(1/d)-m[i])+((m[i]-1)*x[j]*d*(np.log(1-m[i])-np.log(1-np.exp(-1/d)*m[i])))/m[i] #b (-1 + m) (1/(E^(1/d) - m) + (d (Log[1 - m] - Log[1 - E^(-1/d) m]))/ m)

        sol_integral = aux_0 + aux_1 + sum(i for i in aux_2)

        sol_int.append(sol_integral)

    return sum((np.array(rm)-np.array(sol_int))**2)

def opt_fun_instantfuture(x, m,rm,beta0):
    # see mathematica file: yield_curve_model_fit
    beta1 = 0 - beta0
    sol_int = []
    aux_2 = np.zeros(len(x) / 2)
    for i in range(len(m)):
        aux_0 = beta0
        d = x[(len(x) / 2)]
        aux_1 = (beta1*(1-m[i]))/(np.exp(1/d)-m[i])
        for j, val in enumerate(aux_2):
            d = x[(len(x) / 2) + j]
            aux_2[j] = x[j]*(1-m[i])*np.exp(1/d)/(d*(np.exp(1/d)-m[i])**2)
        sol_integral = aux_0 + aux_1 + sum(i for i in aux_2)
        sol_int.append(sol_integral)

    return sum((np.array(rm)-np.array(sol_int))**2)

def rt2rm(y, m):
    # see mathematica file: yield_curve_model_fit
    x = y[2:]
    beta0 = y[0]
    beta1 = y[1]
    # beta1 = 0 - beta0

    sol_int = []
    aux_2 = np.zeros(len(x) / 2)
    for i in range(len(m)):
        aux_0 = beta0
        d = x[(len(x) / 2)]
        aux_1 = ((m[i] - 1) * beta1 * d * (np.log(1 - m[i]) - np.log(1 - np.exp(-1 / d) * m[i]))) / m[
            i]  # (b d (-1 + m) (Log[1 - m] - Log[1 - E^(-1/d) m]))/m
        for j, val in enumerate(aux_2):
            d = x[(len(x) / 2) + j]
            aux_2[j] = (m[i] - 1) * x[j] / (np.exp(1 / d) - m[i]) + (
                        (m[i] - 1) * x[j] * d * (np.log(1 - m[i]) - np.log(1 - np.exp(-1 / d) * m[i]))) / m[
                           i]  # b (-1 + m) (1/(E^(1/d) - m) + (d (Log[1 - m] - Log[1 - E^(-1/d) m]))/ m)

        sol_integral = aux_0 + aux_1 + sum(i for i in aux_2)

        sol_int.append(sol_integral)
    return sol_int


def ycm2rt(y, T):
    # see mathematica file: yield_curve_model_fit
    x=y[2:]
    beta0=y[0]
    beta1 = y[1]
    rt=[]
    aux_2=np.zeros(len(x) / 2)
    for tau in range(T):
        t=tau+1
        aux_0 = beta0
        d= x[(len(x) / 2)]
        aux_1 = beta1*(1-np.exp(-t/d))/(t/d)
        for j, val in enumerate(aux_2):
            d = x[(len(x) / 2) + j]
            aux_2[j]=x[j]*((1-np.exp(-t/d))/(t/d)-np.exp(-t/d))
        rt.append(aux_0+aux_1+ sum(i for i in aux_2))
    return rt