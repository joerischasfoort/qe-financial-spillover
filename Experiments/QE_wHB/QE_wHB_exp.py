import  pickle
import time
import os
import sys
import copy
from multiprocessing import Pool
import pandas


start_time = time.time()

sys.path.append('/home/jriedler/qe-financial-spillover')
#sys.path.append('C:\Users\jrr\Documents\GitHub\qe-financial-spillover')

from spillover_model import *


def helper(args):
    return spillover_model(*args)

hex_home = '/home/jriedler/qe-financial-spillover/Experiments/QE_wHB/'
#hex_home = "C:\Users\jrr\Documents\GitHub\qe-financial-spillover\Experiments\QE_wHB/"
qe_var = [0,200, 500]
ra_var = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]



#when parallel
pos = int(os.getenv('PBS_ARRAYID'))
at=ra_var[pos]



data = open(hex_home + 'Objects_QE_wHB/objects_day_4999_seed_1_RA_' + str(ra_var[pos]) + '.pkl', 'rb')

list_of_objects = pickle.load(data)

portfolios = list_of_objects[0]
currencies = list_of_objects[1]
environment = list_of_objects[2]
exogeneous_agents = list_of_objects[3]
funds = list_of_objects[4]
seed = list_of_objects[5]
obj_label = list_of_objects[6]

data.close()

environment.par.global_parameters["start_day"]=5000
environment.par.global_parameters["end_day"]=6000

environment.par.global_parameters["conv_bound"]=0.001


saving_params = {}
saving_params.update({"path": hex_home + 'Objects_QE_wHB/'})
saving_params.update({"time": 0})


for mlt in qe_var:
    ob_label = "QE" + str(mlt) + "_RA_" + str(at)
    locals()["args_" + str(mlt)] = copy.deepcopy((portfolios,currencies,environment,exogeneous_agents, funds, seed, ob_label, saving_params))

    exec ("args_" + str(mlt) + "[3]['central_bank_domestic'].var.asset_target[args_"+str(mlt) + "[0][0]] = mlt")

    # deepcopy does not seem to copy the index and columns in a pandas dataframe, which leads to errors
    for a in range(len(locals()["args_" + str(mlt)][4])):
        locals()["args_" + str(mlt)][4][a].var.covariance_matrix.index = locals()["args_" + str(mlt)][0] + locals()["args_" + str(mlt)][1]
        locals()["args_" + str(mlt)][4][a].var.covariance_matrix.columns = locals()["args_" + str(mlt)][0] + locals()["args_" + str(mlt)][1]
        locals()["args_" + str(mlt)][4][a].var_previous.covariance_matrix.index = locals()["args_" + str(mlt)][0] + locals()["args_" + str(mlt)][1]
        locals()["args_" + str(mlt)][4][a].var_previous.covariance_matrix.columns = locals()["args_" + str(mlt)][0] + locals()["args_" + str(mlt)][1]


args = ([locals()["args_"+str(mlt)] for mlt in qe_var])

def pool_handler():
    p = Pool(len(qe_var))
    p.map(helper,args)


if __name__ == '__main__':
    pool_handler()
    print("The simulations took", time.time() - start_time, "to run")
	

