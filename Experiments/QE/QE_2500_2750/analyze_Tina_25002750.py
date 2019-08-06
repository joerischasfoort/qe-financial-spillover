import  pickle
import itertools
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools

from helper import *

import_path = '/scratch/kzltin001/qe-financial-spillover'

# Figure out what the objects were called when the simulations were run

start_day = 2499
end_day = 2751


targets = [0, 100, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600]
seeds = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]


analyze = ["fx", "returns","assets","prices","weights","covariance",'default_prob']


# Where are the objects located?
local_dir_mean = "/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_2500_2750/Mean_Cal_Objects/"
local_dir_max = "/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_2500_2750/Max_Cal_Objects/"
local_dir_min = "/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_2500_2750/Min_Cal_Objects/"


filename_QEzero_mean = local_dir_mean + "objects_day_2499_seed_2_2500_2750_med_QE0.pkl"
filename_QEzero_min = local_dir_min + "objects_day_2499_seed_2_2500_2750_min_QE0.pkl"
filename__QEzero_max = local_dir_max + "objects_day_2499_seed_2_2500_2750_max_QE0.pkl"

outputname = 'Tina_raw_and_relative_data_seed_'


# The object_label is defined in the simulation file QE_params_tuple.py
mean_label =  "2500_2750_med_"  + 'QE'
min_label =  "2500_2750_min_"  + 'QE'
max_label =  "2500_2750_max_"  + 'QE'
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
outputfolder = '/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_2500_2750/raw_relative/Mean/'

make_relative_data(filename_QEzero_mean, local_dir_mean, mean_label , targets, seeds , analyze, start_day, end_day , outputname , import_path, outputfolder)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

 
