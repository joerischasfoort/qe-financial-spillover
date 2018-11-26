import  pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from spillover_model_calRA import *
from spillover_model import *
from calibration_functions import *##variables to extract
import pandas as pd



dr00 = []
dr01 = []
dr02 = []
dr03 = []
dr04 = []
dr05 = []


dr10 = []
dr11 = []
dr12 = []
dr13 = []
dr14 = []
dr15 = []

dr20 = []
dr21 = []
dr22 = []
dr23 = []
dr24 = []
dr25 = []

dr30 = []
dr31 = []
dr32 = []
dr33 = []
dr34 = []
dr35 = []

sum_cur0 = []
sum_cur1 = []


path = "C:/Users/jrr/Dropbox/GitHub/qe-financial-spillover/data/Objects_Calibration/"
#path = "Experiments/Risk_Aversion/Objects_RA/"

for day in range(300 , 501):
    filename = path + "objects_day_102_seed_1_4aSim_Cal_"+ str(day)+".pkl"

    # filename = "C:\Users\jrr\Documents\GitHub\qe-financial-spillover\Experiments\QE\Objects_QE1\objects_day_" + str(day) + "_seed_1"  + "_QE_asset_target_1000"+".pkl"
    data = open(filename, "rb")
    list_of_objects = pickle.load(data)

    portfolios = list_of_objects[0]
    currencies = list_of_objects[1]
    environment = list_of_objects[2]
    exogeneous_agents = list_of_objects[3]
    funds = list_of_objects[4]

    dr00.append(funds[0].par.RA_matrix.loc[portfolios[0]][portfolios[0]])
    dr01.append(funds[0].par.RA_matrix.loc[portfolios[1]][portfolios[1]])
    dr02.append(funds[0].par.RA_matrix.loc[portfolios[2]][portfolios[2]])
    dr03.append(funds[0].par.RA_matrix.loc[portfolios[3]][portfolios[3]])
    dr04.append(funds[0].par.RA_matrix.loc[currencies[0]][currencies[0]])
    dr05.append(funds[0].par.RA_matrix.loc[currencies[1]][currencies[1]])

    dr10.append(funds[1].par.RA_matrix.loc[portfolios[0]][portfolios[0]])
    dr11.append(funds[1].par.RA_matrix.loc[portfolios[1]][portfolios[1]])
    dr12.append(funds[1].par.RA_matrix.loc[portfolios[2]][portfolios[2]])
    dr13.append(funds[1].par.RA_matrix.loc[portfolios[3]][portfolios[3]])
    dr14.append(funds[1].par.RA_matrix.loc[currencies[0]][currencies[0]])
    dr15.append(funds[1].par.RA_matrix.loc[currencies[1]][currencies[1]])

    dr20.append(funds[2].par.RA_matrix.loc[portfolios[0]][portfolios[0]])
    dr21.append(funds[2].par.RA_matrix.loc[portfolios[1]][portfolios[1]])
    dr22.append(funds[2].par.RA_matrix.loc[portfolios[2]][portfolios[2]])
    dr23.append(funds[2].par.RA_matrix.loc[portfolios[3]][portfolios[3]])
    dr24.append(funds[2].par.RA_matrix.loc[currencies[0]][currencies[0]])
    dr25.append(funds[2].par.RA_matrix.loc[currencies[1]][currencies[1]])

    dr30.append(funds[3].par.RA_matrix.loc[portfolios[0]][portfolios[0]])
    dr31.append(funds[3].par.RA_matrix.loc[portfolios[1]][portfolios[1]])
    dr32.append(funds[3].par.RA_matrix.loc[portfolios[2]][portfolios[2]])
    dr33.append(funds[3].par.RA_matrix.loc[portfolios[3]][portfolios[3]])
    dr34.append(funds[3].par.RA_matrix.loc[currencies[0]][currencies[0]])
    dr35.append(funds[3].par.RA_matrix.loc[currencies[1]][currencies[1]])

    sum_cur0.append(dr04[-1]+dr14[-1]+dr24[-1]+dr34[-1])
    sum_cur1.append(dr05[-1]+dr15[-1]+dr25[-1]+dr35[-1])


sum_cur = (np.array(sum_cur0) + np.array(sum_cur1)).tolist()

index_min = sum_cur.index(min(sum_cur)) + 300
index_max = sum_cur.index(max(sum_cur)) + 300
index_med = sum_cur.index( sorted(sum_cur)[len(sum_cur) / 2]) + 300