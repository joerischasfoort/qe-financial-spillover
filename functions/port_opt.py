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




        ###########################################################################
        ################## COMPUTING ALL SOLUTION PATHS ###########################
        ############################################################################
        tree = {}
        counter = {}
        stored_aux_cov = {}
        stored_aux_ret = {}
        stored_test = {}
        stored_weights = {}
        shorted = []
        layer = 0
        counter[layer] = 0
        solution_number = 0



        for ind, val in enumerate(test):
            if val == True:
                shorted.append(ind)

        tree[layer] = shorted
        stored_test[layer] = test.copy()
        stored_weights[layer] = weights.copy()
        stored_aux_cov[layer] = aux_cov.copy()
        stored_aux_ret[layer] = aux_ret.copy()
        solution_path = {}
        solution_weights = {}


        while layer >= 0:
            while sum(test) > 0:
                aux_cov[tree[layer][counter[layer]], :] = 0
                aux_cov[tree[layer][counter[layer]], tree[layer][counter[layer]]] = 1
                aux_ret[tree[layer][counter[layer]]] = 0
                # recompute compute matrix inverse and weights
                inv_aux_cov = np.linalg.inv(aux_cov)
                weights = np.matmul(inv_aux_cov, aux_ret) * (1 / float(risk_aversion))
                test = weights[:-1] < -1e-10
                layer += 1

                shorted = []
                for ind, val in enumerate(test):
                    if val == True:
                        shorted.append(ind)
                tree[layer] = shorted
                stored_test[layer] = test.copy()
                stored_weights[layer] = weights.copy()
                stored_aux_cov[layer] = aux_cov.copy()
                stored_aux_ret[layer] = aux_ret.copy()
                counter[layer] = 0

            # storing the a possible solution
            solution_path[solution_number] = [tree[l][counter[l]] for l in range(layer)]
            solution_weights[solution_number] = weights
            solution_number += 1

            layer -= 1
            # check if we are on the the highest level: if we are, all solutions have been stored
            if layer < 0:
                break

            aux = False
            while aux == False:
                #check if all solutions of one layer have been computed
                if counter[layer]== len(tree[layer])-1 and layer>0: # if yes, go back one layer
                    layer -= 1
                if counter[layer] != len(tree[layer])-1 and layer >= 0: # if no, increase the counter of that layer and restore variables of the layer
                    counter[layer] += 1
                    test = stored_test[layer]
                    weights = stored_weights[layer].copy()
                    aux_cov = stored_aux_cov[layer].copy()
                    aux_ret = stored_aux_ret[layer].copy()
                    aux = True
                if layer == 0:
                    aux = True


        ##############################################################
        ##############################################################

        # compute utility
        U = {}
        Utility = []
        for sol in range(len(solution_weights)):
            for i in range(len(E_ret_assets)):
                U[i] = solution_weights[sol][i] * E_ret_assets[i] - 0.5 * risk_aversion * sum(
                    [(solution_weights[sol][j] * solution_weights[sol][i]) * Cov_assets.iloc[i, j] for j in range(len(E_ret_assets))])
            Utility.append(sum(U.values()))
        weights = solution_weights[Utility.index(max(Utility))]



        output = {}


        for i, a in enumerate(Cov_assets.columns.values):
            output[a] = weights[i]
        
        return output