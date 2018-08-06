import numpy as np
import pandas as pd

def portfolio_optimization_KT(f):
    
        #create a copy of the covariance matrix of the funds
        Cov_assets = f.var.covariance_matrix.copy()
        #
        E_ret_assets = np.zeros((len(Cov_assets)))  

        #compute the risk aversion matrix
        risk_aversion_mat = f.var.covariance_matrix.copy()
        for row in Cov_assets.index:
            for col in Cov_assets.columns:
                risk_aversion_mat.loc[row,col]=np.sqrt(f.par.risk_aversion[row.par.country + "_assets"])*np.sqrt(f.par.risk_aversion[col.par.country +"_assets"])
        

        #multiply covariance with asset specific risk aversion
        Cov_assets = np.multiply(Cov_assets, risk_aversion_mat)
        original_cov = np.array(Cov_assets)

        # Create a 1D numpy array with one expected returns per asset
        for i, a in enumerate(Cov_assets.columns.values):
                E_ret_assets[i] = f.exp.returns[a]

        
        # adding the budget constraint to the covariance matrix - to solve the model using linear algebra
        # Adding a row with ones 
        aux_cov = np.concatenate((Cov_assets,np.ones((1,len(Cov_assets)))),axis=0)
        
        # Adding a column with ones 
        aux_cov = np.concatenate((aux_cov,np.ones((len(aux_cov),1))),axis=1) 
    
        aux_cov[len(aux_cov)-1,len(aux_cov)-1] = 0
        
        # adding the budget constraint to the return vector - to solve the model using linear algebra
        aux_x=np.append(E_ret_assets,0)
        aux_y = np.zeros(len(aux_x))
        aux_y[len(aux_x)-1]=1


        # compute matrix inverse
        inv_aux_cov=np.linalg.inv(aux_cov)
        aux_c = np.matmul(inv_aux_cov, aux_x)
        aux_d = np.matmul(inv_aux_cov, aux_y)
        
        # solving for optimal weights
        weights=aux_c + aux_d
        original_weights = weights.copy()

        # Start of algorithm that takes out shorted assets   
        test = weights[:-1] < 0

        while sum(test)>0:
            for i in range(len(aux_cov)):
                for j in range(len(aux_cov)):
                    if weights[i] < 0 and i != j:
                        aux_cov[i,j] = 0
                    if weights[i] < 0 and i == j:
                        aux_cov[i, j] = 1
            for i in range(len(aux_x)-1):
                if weights[i] < 0:
                    aux_x[i]=0
                    aux_y[i]=0

            # compute matrix inverse
            inv_aux_cov=np.linalg.inv(aux_cov)
            aux_c = np.matmul(inv_aux_cov, aux_x)
            aux_d = np.matmul(inv_aux_cov, aux_y)

            weights=aux_c + aux_d
            test = weights[:-1] < 0

        aux_e = np.zeros(len(aux_c)-1)
        aux_f = np.zeros(len(aux_c)-1)
        for i in range(len(aux_e)):
            aux_e[i]=E_ret_assets[i]-sum([original_cov[i,j]*aux_c[j] for j in range(len(aux_e))])-aux_c[-1]
            aux_f[i]=sum([original_cov[i,j]*aux_d[j] for j in range(len(aux_e))])+aux_d[-1]

        aux_KT_pd = aux_e-aux_f #partial derivatives
        test_KT = np.zeros(len(aux_KT_pd))
        for i in range(len(aux_KT_pd)):
            if weights[i]>0:
                test_KT[i] = aux_KT_pd[i] == 0
            else:
                test_KT[i] = aux_KT_pd[i] <= 0

        if sum(test_KT)<len(test_KT):
            print 'why?'


        output = {}



        for i, a in enumerate(Cov_assets.columns.values):
            output[a] = weights[i]


        return  output