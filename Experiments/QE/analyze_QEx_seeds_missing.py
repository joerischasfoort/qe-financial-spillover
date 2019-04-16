import  pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import itertools
import sys

sys.path.append('/scratch/kzltin001/qe-financial-spillover')

from functions.analysis_functions import *
 
start_day = 2500
end_day = 3504

# assets_target = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600]
variable = []
for i in range(0,2500, 100):
   variable.append(i)

#20seeds
seeds = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

analyze = ["fx", "returns","assets","prices","weights","covariance",'default_prob']


local_dir = "/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_3500/Med_3500/Objects_Tina_3500/"


filename = local_dir + "objects_day_2500_seed_2_Tina_3500med_QE0.pkl"


data = open(filename, "rb")
list_of_objects = pickle.load(data)

portfolios = list_of_objects[0]
currencies = list_of_objects[1]
environment = list_of_objects[2]
exogeneous_agents = list_of_objects[3]
funds = list_of_objects[4]


for seed in seeds:
	
	benchmark =  "_seed_" +str(seed) +"_Tina_3500med_QE0"
	raw_data = {}
	ordered_var_list = []
 
	
	for i in variable:
		obj_label =  "QE_med_" + str(i)
		obj_label = "_seed_" +str(seed)  +"_Tina_3500med_QE" + str(i)
		
		for day in range(start_day,end_day+1):
			 
			filename = local_dir + "objects_day_" + str(day) + obj_label+".pkl"
			try: 
				data = open(filename,"rb")
				raw_data.update({obj_label: creating_lists(analyze, funds, portfolios,currencies, environment,exogeneous_agents)})
				ordered_var_list.append(obj_label)
			except IOError:
				print 'error'
				continue


	for i in variable:
		obj_label =  "QE_med_" + str(i)
		obj_label = "_seed_" +str(seed)  +"_Tina_3500med_QE" + str(i)
		
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

			except IOError:
				#print 'error_dumping'
				continue			

	print i  , 'did we get here?' 

	try:

		relative_data, raw_data2 =  relative_development(raw_data, benchmark)
		list_of_objects = [seed, raw_data2, relative_data]
		print seed
		file_name2 = '3500_Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'
		save_objects = open(file_name2, 'wb')
		pickle.dump(list_of_objects, save_objects)
		save_objects.close()
		print 'DONE.'
	except:
		print 'seed' , seed, 'doesn t work noooo' 
		continue
 
