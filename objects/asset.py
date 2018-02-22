class Asset():
    """Asset type class"""
    def __init__(self, variables, previous_variables, parameters):
        self.var = variables
        self.var_previous =  previous_variables
        self.par = parameters