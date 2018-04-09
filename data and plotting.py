import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.plot(x)




import pickle

data = open('objects.pkl', 'wb')
seed=1
testing = [portfolios, currencies, environment, exogeneous_agents, funds, seed]

pickle.dump(testing,data)

data.close()


