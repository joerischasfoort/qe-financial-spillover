import numpy as np

def portfolio_optimization(E_ret_assets, Cov_assets, E_ret_cash, risk_aversion):
    
    ## some random sample values to test the function
    Cov_assets = np.random.rand(5,5)
    # making the sample covariance matrix symmetric
    for i in range(len(Cov_assets)):
        for j in range(len(Cov_assets)):
            if j != i:
                Cov_assets[i,j]=Cov_assets[j,i]
                
    E_ret_assets =np.random.rand(5) 
    E_ret_cash = np.array([0])
    risk_aversion = np.array([2])
    ## the real function starts here
    
    for f in funds:
        Cov_assets = 
    
    # adding cash to the covariance matrix
    aux_cov = np.concatenate((Cov_assets, np.zeros((1,len(Cov_assets)))),axis=0)
    aux_cov = np.concatenate((aux_cov, np.zeros((len(aux_cov),1))),axis=1)
    
    # adding the budget constraint to the covariance matrix - to solve the model using linear algebra
    aux_cov = np.concatenate((aux_cov,np.ones((1,len(aux_cov)))),axis=0)
    aux_cov = np.concatenate((aux_cov,np.ones((len(aux_cov),1))),axis=1) 
    aux_cov[len(aux_cov)-1,len(aux_cov)-1] = 0
    
    # adding cash to the return vector
    aux_ret=np.concatenate((E_ret_assets,E_ret_cash),axis=0)
    
    # adding the budget constraint to the return vector - to solve the model using linear algebra
    aux_ret=np.concatenate((aux_ret,risk_aversion),axis=0)
    
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
        # recompute compute matrix inverse and weights
        inv_aux_cov=np.linalg.inv(aux_cov)
        weights=np.matmul(inv_aux_cov, aux_ret)*(1/float(risk_aversion))      
        test = weights[:-1] < 0       
            
    
    return weights