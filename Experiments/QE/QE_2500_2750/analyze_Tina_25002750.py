import  pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools
import sys
import os

sys.path.append('/Users/Tina/git_repos/qe-financial-spillover/') # path to root directory

from functions.analysis_functions import *
from functions.helper import *
 

"Which seeds, QE targets and days were simulated?"
days =list(range(2500,2750+1))

targets = [0, 100, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600]
seeds = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]


analyze = ["fx", "returns","assets","prices","weights","covariance",'default_prob']

experiment_dir = "/Users/Tina/git_repos/qe-financial-spillover/Experiments/QE/QE_2500_2750/"
object_dir = "/Users/Tina/git_repos/qe-financial-spillover/Experiments/QE/QE_2500_2750/Med_Cal_Objects/"


"WHERE IS THE BENCHMARK?"
filename =  "/Users/Tina/git_repos/qe-financial-spillover/Experiments/QE/QE_2500_2750/Med_Cal_Objects/objects_day_2499_seed_2_2500_2750_med_QE0.pkl"
label = '_2500_2750_med_QE' #  object label specified in the simulation file

make_relative_data(filename, targets, seeds,days, analyze, experiment_dir , object_dir, label,  '/Users/Tina/git_repos/qe-financial-spillover/', 'raw_relative/test/', printarg='yes')
 
 
#    data_mean, data_p5, data_p95  = compute_averages(relative_data,benchmark, ordered_var_list, range(900,999))

	 
print('DONE MUHAHAHAHA!')

 