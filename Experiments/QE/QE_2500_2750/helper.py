
import pandas as pd
import pickle
import itertools




def make_relative_data(filename_zero, local_dir, label, targets, seeds, analyze, start_day , end_day, outputname, import_path, outputfolder):
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


	for seed in seeds:
		benchmark =  "_seed_" +str(seed) + label+'0'
		raw_data = {}
		ordered_var_list = []
		for i in targets:
			obj_label = "_seed_" +str(seed)  +"_"+ label + str(i)
			for day in range(start_day,end_day+1):
				 
				filename = local_dir + "objects_day_" + str(day) + obj_label+".pkl"
				try: 
					data = open(filename,"rb")
					raw_data.update({obj_label: creating_lists(analyze, funds, portfolios,currencies, environment,exogeneous_agents)})
					ordered_var_list.append(obj_label)
				except IOError:
					print 'error'
					continue


		for i in targets:
			obj_label = "_seed_" +str(seed)  +"_" + label + str(i)
			
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

		try:

			relative_data, raw_data2 =  relative_development(raw_data, benchmark)
			list_of_objects = [seed, raw_data2, relative_data]
		# 	    #    data_mean, data_p5, data_p95  = compute_averages(relative_data,benchmark, ordered_var_list, range(900,999))
			print seed
			file_name2 = outputfolder +outputname  + label+ str(seed) + '.pkl'
			save_objects = open(file_name2, 'wb')
			pickle.dump(list_of_objects, save_objects)
			save_objects.close()
			print 'DONE MUHAHAHAHA.'
		except:
			print 'seed' , seed, 'doesn t work noooo' 
			continue


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