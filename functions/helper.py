
import pandas as pd
import pickle
import itertools
import os

import pandas as pd
import pickle
import itertools
import os



def make_relative_data(filename_zero,  targets, seeds,days ,analyze, experiment_dir , object_dir, label, import_path, outputfolder, printarg):
	# Be careful how to import analysis_functions.py and use the right path!!
	import sys
	sys.path.append(import_path)

	from functions.analysis_functions import creating_lists, add_observations, relative_development


	data = open(filename_zero, "rb")
	list_of_objects = pickle.load(data)

	portfolios = list_of_objects[0]
	currencies = list_of_objects[1]
	environment = list_of_objects[2]
	exogeneous_agents = list_of_objects[3]
	funds = list_of_objects[4]

	"First,let's check if all seeds exist and drop those one" #  More elegant solution?  USE OS!! 
	for seed in seeds:
		try:
			obj_label = "_seed_" +str(seed)  + label + str(targets[0]) 
			filename = object_dir + "objects_day_" + str(days[0]) + obj_label+".pkl"
			data = open(filename,"rb")
		except:
			print("ATTENTION seed" , seed,"doesn't exist and will be dropped from seed list")
			seeds.remove(seed)
			continue

	"Second, check the targets that worked for the seeds" #  More elegant solution?
 	files = [f for f in os.listdir(object_dir)]

 	for seed in seeds:
		benchmark =  "_seed_" +str(seed) +label+"0"
		raw_data = {}
		ordered_var_list = []

 		temp = []
 		for f in files:
 			if 'seed_'+str(seed) in f:
				temp.append(f.split("QE",1)[1][:-4])
		myset = set(temp)
		new_targets = list(myset)
		print('Seed', seed, 'has these targets', new_targets)

		for i in new_targets:
			obj_label = "_seed_" +str(seed)  +label + str(i)
			ordered_var_list.append(obj_label)
			raw_data.update({obj_label: creating_lists(analyze, funds, portfolios,currencies, environment,exogeneous_agents)})

			for day in days:
				filename = object_dir + "objects_day_" + str(day) + obj_label+".pkl"
				data = open(filename,"rb")
				list_of_objects = pickle.load(data)
				portfolios = list_of_objects[0]
				currencies = list_of_objects[1]
				environment = list_of_objects[2]
				exogeneous_agents = list_of_objects[3]
				funds = list_of_objects[4]

				raw_data[obj_label] = add_observations(raw_data[obj_label], funds, portfolios,currencies, environment,exogeneous_agents)

				if day==days[-1] and i == new_targets[-1]:
					print('All days for seed', seed, 'processed')

		relative_data =  relative_development(raw_data, benchmark)
		file_name = experiment_dir + outputfolder+label+'Tina_raw_and_relative_data_seed_' + str(seed)+ '.pkl'     #  ATTENTION ERROR SOURCE HERE 
		save_objects = open(file_name, 'wb')
		list_of_objects = [seed, raw_data, relative_data]
		pickle.dump(list_of_objects, save_objects)
		save_objects.close()
		if printarg=='yes':
			print(file_name+' was written, YAY!')

 

def read_data(pickl_dir, seeds, important_filelabel, var_list, label_zero):
	df = pd.DataFrame()
	df_list = []

	files = [f for f in os.listdir(pickl_dir)]

	temp = []

	print seeds

	for seed in seeds:
	    for f in files:
	        if 'seed_'+str(seed) in f:
	        	print f
	        	temp.append(f.split("seed_",1)[1])   


	myset = set(temp)
	new_seeds = list(myset)



	print('############# Reading bond and equity returns..########')
    
	for seed in seeds:

		filename = pickl_dir + important_filelabel + str(seed)  + '.pkl'
		try:

			data = open(filename, "rb")
			list_of_objects = pickle.load(data)
			seedx = list_of_objects[0]
			raw_data = list_of_objects[1]
			relative_data = list_of_objects[2]
			print filename
 
			"Make change variables: be careful with label zero. It depends how the QE-0 label was saved!"
			for key, value in relative_data.items():
				relative_data[key]['percentage_portfolio2'] = relative_data[key]['portfolios[2].var.price'] / raw_data['_seed_' +str(seed)  + label_zero]['portfolios[2].var.price'] * 100
				relative_data[key]['percentage_portfolio1'] = relative_data[key]['portfolios[1].var.price'] / raw_data['_seed_' +str(seed)  + label_zero]['portfolios[1].var.price'] * 100
				relative_data[key]['percentage_portfolio0'] = relative_data[key]['portfolios[0].var.price'] / raw_data['_seed_' +str(seed)  + label_zero]['portfolios[0].var.price'] * 100
				relative_data[key]['percentage_portfolio3'] = relative_data[key]['portfolios[3].var.price'] / raw_data['_seed_' +str(seed)  + label_zero]['portfolios[3].var.price'] * 100
				relative_data[key]['percentage_fx_rates.iloc[0,1]'] = relative_data[key]['environment.var.fx_rates.iloc[0,1]'] / raw_data['_seed_' +str(seed)  + label_zero]['environment.var.fx_rates.iloc[0,1]'] * 100
			rows = []
	 

			for qe, assets in relative_data.items():
				all = {}
				for key_asset, var in assets.items():
					if key_asset in var_list:
						for time, val in enumerate(var):
							all = {}
							all['seed'] = seed
							list_temp = []
							list_temp.append(qe)
							"ATTENTION!!! - This drags out the QE, but it depends on len(string)"
							all['QE'] = list_temp[0][qe.find('_',18 ) + 3:]
							all['asset'] = key_asset
							all['val'] = val
							all['time'] = time
							rows.append(all)
			temp = pd.DataFrame(rows) # all times per experiment
			df_list.append(temp) # all data per seed
		except:
			print("problem with "+filename)
	df = pd.concat(df_list, keys=seeds , sort=True)  # concat seeds
	return df
 
