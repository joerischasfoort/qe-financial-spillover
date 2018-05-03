
import  pickle
import pp, time
import multiprocessing
from spillover_model import *
import os

from multiprocessing import Process



data = open('data/Objects/objects_start.pkl', 'rb')
#data = open('data/Objects/objects_nonConv_day8890.pkl', 'rb')

list_of_objects = pickle.load(data)

portfolios = list_of_objects[0]
currencies = list_of_objects[1]
environment = list_of_objects[2]
exogeneous_agents = list_of_objects[3]
funds = list_of_objects[4]
seed = list_of_objects[5]

data.close()

environment.par.global_parameters["start_day"]=12000
environment.par.global_parameters["end_day"]=12010

start_time = time.time()


if __name__ == '__main__':
    seed = range(1,20)
    procs = []

    for index, number in enumerate(seed):
        proc = Process(target=spillover_model, args=(portfolios, currencies, environment, exogeneous_agents, funds,  number))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
print "parallel: Time elapsed: ", time.time() - start_time, "s"


#start_time = time.time()
#for seed in [5, 10, 15, 20, 25]:
#    spillover_model(portfolios, currencies, environment, exogeneous_agents, funds, seed)
#print "serial: Time elapsed: ", time.time() - start_time, "s"