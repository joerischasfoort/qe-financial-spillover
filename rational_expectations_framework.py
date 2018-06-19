import  pickle
import os.path
import numpy as np
from rational_expectations_functions import *




# setting overarching parameters
local_dir = "Experiments/Maturity/Objects_MAT/"
obj_label = "mat_1"
seed_range = [1]
time_range = range(4000, 5000)



check_file_availability(local_dir, obj_label, time_range, seed_range)


