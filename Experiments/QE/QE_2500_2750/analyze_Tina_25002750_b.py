import  pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools
import sys
import os

sys.path.append('/Users/Tina/git_repos/qe-financial-spillover/')

from functions.analysis_functions import *
 

start_day = 2499
end_day = 2750

variable = [0, 100, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600]
seeds = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

 

analyze = ["fx", "returns","assets","prices","weights","covariance",'default_prob']
#benchmark = "QE_med_0"

local_dir = "/Users/Tina/git_repos/qe-financial-spillover/Experiments/QE/QE_2500_2750/Med_Cal_Objects/"
filename =  "/Users/Tina/git_repos/qe-financial-spillover/Experiments/QE/QE_2500_2750/Med_Cal_Objects/objects_day_2499_seed_2_2500_2750_med_QE0.pkl"

data = open(filename, "rb")
list_of_objects = pickle.load(data)

portfolios = list_of_objects[0]
currencies = list_of_objects[1]
environment = list_of_objects[2]
exogeneous_agents = list_of_objects[3]
funds = list_of_objects[4]


for seed in seeds:
	
	benchmark =  "_seed_" +str(seed) + "_2500_2750_med_QE0"
	raw_data = {}
	ordered_var_list = []
 
 	print seed
	
	
	for i in variable:
		# obj_label =  "QE_med_" + str(i)
		obj_label = "_seed_" +str(seed)  +"_2500_2750_med_QE" + str(i)

		day = start_day
		i  = variable[0]
		filename = local_dir + "objects_day_" + str(day) + obj_label+".pkl"

		for day in range(start_day,end_day+1):
			 
			filename = local_dir + "objects_day_" + str(day) + obj_label+".pkl"
			
			try: 
				data = open(filename,"rb")
 				raw_data.update({obj_label: creating_lists(analyze, funds, portfolios,currencies, environment,exogeneous_agents)})
				ordered_var_list.append(obj_label)
 			except IOError:
				print 'error', filename
  				continue
        

	for i in variable:
		# obj_label =  "QE_min_" + str(i)
		obj_label = "_seed_" +str(seed)  +"_2500_2750_med_QE" + str(i)
		
		for day in range(start_day,end_day+1):
			 
			filename = local_dir + "objects_day_" + str(day) + obj_label+".pkl"
			try: 
				data = open(filename,"rb")
				
				list_of_objects = pickle.load(data)
				portfolios = list_of_objects[0]

				currencies = list_of_objects[1]
				environment = list_of_objects[2]
				exogeneous_agents = list_of_objects[3]
				funds = list_of_objects[4]
				raw_data[obj_label] = add_observations( raw_data[obj_label], funds, portfolios,currencies, environment,exogeneous_agents)
				#print 'hereeeeee', obj_label, i, day

			except IOError:
				#print 'error_dumping'
				continue			


	try:

		relative_data, raw_data2 =  relative_development(raw_data, benchmark)
		list_of_objects = [seed, raw_data2, relative_data]
	# 	    #    data_mean, data_p5, data_p95  = compute_averages(relative_data,benchmark, ordered_var_list, range(900,999))
		print seed
		file_name2 = '/Users/Tina/git_repos/qe-financial-spillover/Experiments/QE/QE_2500_2750/test/med_25002750_Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'
		save_objects = open(file_name2, 'wb')
		pickle.dump(list_of_objects, save_objects)
		save_objects.close()
		print 'DONE MUHAHAHAHA.'
	except:
		print 'seed' , seed, 'doesn t work noooo' 
		continue


