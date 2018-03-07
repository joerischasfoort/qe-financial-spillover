class Environment():
    """Class holding environment properties"""
    def __init__(self, variables, previous_variables, parameters):
        self.var = variables
        self.var_previous = previous_variables
        self.par = parameters

    def __repr__(self):
        return 'environment'


class EnvironmentVariables:
    """
    Holds a matrix of exchange rates
    """
    def __init__(self, fx_rates):
        self.fx_rates = fx_rates


class EnvironmentParameters:
    """
    Holds the global parameters in a dictionary
    """
    def __init__(self, global_parameters):
        self.global_parameters = global_parameters