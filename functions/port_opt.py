import numpy as np
import pandas as pd

def portfolio_optimization(f):
    

        
    Cov_assets = f.var.covariance_matrix.copy()
    
    E_ret_assets = np.zeros((len(Cov_assets)))   
    for i, a in enumerate(Cov_assets.columns.values):
            E_ret_assets[i] = f.exp.returns[a]

        
    risk_aversion = f.par.risk_aversion
    
    
    # adding the budget constraint to the covariance matrix - to solve the model using linear algebra
    aux_cov = np.concatenate((Cov_assets,np.ones((1,len(Cov_assets)))),axis=0)
    aux_cov = np.concatenate((aux_cov,np.ones((len(aux_cov),1))),axis=1) 
    aux_cov[len(aux_cov)-1,len(aux_cov)-1] = 0
    
    
    # adding the budget constraint to the return vector - to solve the model using linear algebra
    aux_ret=np.append(E_ret_assets,risk_aversion)
    
    # compute matrix inverse
    inv_aux_cov=np.linalg.inv(aux_cov)
    
    # solving for optimal weights
    weights=np.matmul(inv_aux_cov, aux_ret)*(1/float(risk_aversion))
    
    # Start of algorithm that takes out shorted assets   
    test = weights[:-1] < 0 
    
    while sum(test)>0:   
        for i in range(len(test)):
            if test[i]==True: 
               aux_cov[i,:]=0
               aux_cov[i,i]=1
               aux_ret[i]=0
        # recompute compute matrix inverse and weights
        inv_aux_cov=np.linalg.inv(aux_cov)
        weights=np.matmul(inv_aux_cov, aux_ret)*(1/float(risk_aversion))      
        test = weights[:-1] < 0       
    output = {}    
    for i, a in enumerate(Cov_assets.columns.values):
        output[a] = weights[i]
    

    return output