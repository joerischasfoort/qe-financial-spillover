import codecs
import time
import multiprocessing
from spillover_model import *
import os
import pandas as pd

from multiprocessing import Process

#Python 2.7!!!
import cPickle

data = open('/home/kzltin001/qe/data/Objects/objects_start.pkl', 'rb')

list_of_objects = cPickle.load(data)


portfolios = list_of_objects[0]
currencies = list_of_objects[1]
environment = list_of_objects[2]
exogeneous_agents = list_of_objects[3]
funds = list_of_objects[4]
seed = list_of_objects[5]

data.close()

environment.par.global_parameters["start_day"]=1
environment.par.global_parameters["end_day"]=100

#start_time = time.time()


if __name__ == '__main__':
    seed = range(1,100)
    procs = []

    for index, number in enumerate(seed):
        proc = Process(target=spillover_model, args=(portfolios, currencies, environment, exogeneous_agents, funds,  number))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

#print "parallel: Time elapsed: ", time.time() - start_time, "s"


#start_time = time.time()
#for seed in [5, 10, 15, 20, 25]:
#    spillover_model(portfolios, currencies, environment, exogeneous_agents, funds, seed)
#print "serial: Time elapsed: ", time.time() - start_time, "s"
