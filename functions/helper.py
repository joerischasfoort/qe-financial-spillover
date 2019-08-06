
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

				if day==days[-1] and i == targets[-1]:
					print('All days for seed', seed, 'processed')

		relative_data =  relative_development(raw_data, benchmark)
		file_name = experiment_dir + outputfolder+label+'Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'     #  ATTENTION ERROR SOURCE HERE 
		save_objects = open(file_name, 'wb')
		list_of_objects = [seed, raw_data, relative_data]
		pickle.dump(list_of_objects, save_objects)
		save_objects.close()
		if printarg=='yes':
			print(file_name+'was written, YAY!')

 
 
	

	# for seed in seeds:
	# 	benchmark =  "_seed_" +str(seed) +label+"0"
	# 	raw_data = {}
	# 	ordered_var_list = []

	# 	for i in targets:
	# 		obj_label = "_seed_" +str(seed)  +label + str(i)
	# 		ordered_var_list.append(obj_label)
	# 		raw_data.update({obj_label: creating_lists(analyze, funds, portfolios,currencies, environment,exogeneous_agents)})

	# 		for day in days:
	# 			filename = object_dir + "objects_day_" + str(day) + obj_label+".pkl"
	# 			data = open(filename,"rb")
	# 			list_of_objects = pickle.load(data)
	# 			portfolios = list_of_objects[0]
	# 			currencies = list_of_objects[1]
	# 			environment = list_of_objects[2]
	# 			exogeneous_agents = list_of_objects[3]
	# 			funds = list_of_objects[4]

	# 			raw_data[obj_label] = add_observations(raw_data[obj_label], funds, portfolios,currencies, environment,exogeneous_agents)

	# 			if day==days[-1] and i == targets[-1]:
	# 				print('All days for seed', seed, 'processed')

	# 	relative_data =  relative_development(raw_data, benchmark)
	# 	file_name = experiment_dir + 'raw_relative/test/'+label+'Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'     #  ATTENTION ERROR SOURCE HERE 
	# 	save_objects = open(file_name, 'wb')
	# 	list_of_objects = [seed, raw_data, relative_data]
	# 	pickle.dump(list_of_objects, save_objects)
	# 	save_objects.close()

def read_return_data(local_dir, label, seeds, var_list_returns):

	print('############# Reading bond and equity returns..########')
	for seed in seeds:
	    filename = local_dir + 'MEAN_25002750_Tina_raw_and_relative_data_seed_' + str(seed) + '.pkl'
	    data = open(filename, "rb")
	    list_of_objects = pickle.load(data)
	    seedx = list_of_objects[0]
	    raw_data = list_of_objects[1]
	    relative_data = list_of_objects[2]
	    print seed, 'returns data'

	    rows = []

	    for qe, assets in relative_data.items():
	        all = {}
	        #
	        for key_asset, var in assets.items():
	            if key_asset in var_list_returns:
	                #print key_asset
	                for time, val in enumerate(var):
	                    all = {}
	                    all['seed'] = seed

	                    list_temp = []
	                    list_temp.append(qe)

	                    #print list_temp[0][qe.find('_', 10):] This drags out the QE

	                    all['QE'] = list_temp[0][qe.find('_', 13) + 3:]
	                    all['asset'] = key_asset
	                    all['val'] = val
	                    all['time'] = time
	                    #print time
	                    rows.append(all)

	    temp = pd.DataFrame(rows) # all times per experiment
	    df_list.append(temp) # all data per seed
	df_exp_returns = pd.concat(df_list, keys=seeds , sort=True)  # concat seeds
	return df_exp_returns