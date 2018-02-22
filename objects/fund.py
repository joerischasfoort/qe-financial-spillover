class Fund():
    """Class holding fund properties"""
    def __init__(self, variables, previous_variables, parameters):
        self.var = variables
        self.var_previous = previous_variables
        self.par = parameters