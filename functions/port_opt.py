import numpy as np
import pandas as pd

def portfolio_optimization(f):
    
        #create a copy of the covariance matrix of the funds
        Cov_assets = f.var.covariance_matrix.copy()
        #
        E_ret_assets = np.zeros((len(Cov_assets)))  
        
        
        # Create a 1D numpy array with one expected returns per asset  
        for i, a in enumerate(Cov_assets.columns.values):
                E_ret_assets[i] = f.exp.returns[a]

        risk_aversion = f.par.risk_aversion
        
        # adding the budget constraint to the covariance matrix - to solve the model using linear algebra
        # Adding a row with ones 
        aux_cov = np.concatenate((Cov_assets,np.ones((1,len(Cov_assets)))),axis=0)
        
        # Adding a column with ones 
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
        #the idea is to take out shorted assets in the order of the size of their partial derivatives (under the assumptions that the agent holds a marginal amount of each asset)

        #derivatives = [E_ret_assets[i]-risk_aversion*sum([Cov_assets.iloc[i,j]*0.0000001 for j in range(len(E_ret_assets))]) for i in range(len(E_ret_assets))]
        w = [weights[i] if test[i]==False else 0.0000001 for i in range(len(E_ret_assets))]
        derivatives_new = [E_ret_assets[i]-risk_aversion*sum([Cov_assets.iloc[i,j]*w[j] for j in range(len(E_ret_assets))]) for i in range(len(E_ret_assets))]
        select_derivative_new = [max(derivatives_new)+1 if test[i]==False else derivatives_new[i] for i in range(len(derivatives_new))]

        #select_derivative = [max(derivatives)+1 if test[i]==False else derivatives[i] for i in range(len(derivatives))]

        while sum(test)>0:
            i = np.argmin(select_derivative_new)
            if test[i]==True:
               aux_cov[i,:]=0
               aux_cov[i,i]=1
               aux_ret[i]=0
            # recompute compute matrix inverse and weights
            inv_aux_cov=np.linalg.inv(aux_cov)
            weights=np.matmul(inv_aux_cov, aux_ret)*(1/float(risk_aversion))      
            test = weights[:-1] < -1e-10
            #select_derivative = [max(derivatives)+1 if test[i] == False else derivatives[i] for i in range(len(derivatives))]
            w = [weights[i] if test[i] == False else 0.0000001 for i in range(len(E_ret_assets))]
            derivatives_new = [E_ret_assets[i] - risk_aversion * sum([Cov_assets.iloc[i, j] * w[j] for j in range(len(E_ret_assets))]) for i in range(len(E_ret_assets))]
            select_derivative_new = [max(derivatives_new) + 1 if test[i] == False else derivatives_new[i] for i in range(len(derivatives_new))]

        output = {}

        for i, a in enumerate(Cov_assets.columns.values):
            output[a] = weights[i]
        
        return output