from objects.environment import *
import numpy as np
import pandas as pd

def init_environment(currencies, parameters):

    fx_matrix = np.zeros([len(currencies), len(currencies)])
    fx_matrix = pd.DataFrame(fx_matrix, index=currencies, columns=currencies)

    for c1, c2 in zip(currencies, currencies[::-1]):
        fx = parameters["init_exchange_rate"]
        if c1.par.country == 'foreign':
            fx = 1 / fx
        fx_matrix.loc[c1, c2] = fx
        fx_matrix.loc[c1, c1] = 1

    currency_countries = {c: c.par.country for c in currencies}
    fx_matrix.rename(index=currency_countries, inplace=True)
    fx_matrix.rename(columns=currency_countries, inplace=True)

    environment = Environment(EnvironmentVariables(fx_matrix,fx_matrix.copy()), EnvironmentVariables(fx_matrix.copy(),fx_matrix.copy()),
                              EnvironmentParameters(parameters))

    return environment