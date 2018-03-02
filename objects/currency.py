class Currency():
    """Currency type class"""
    def __init__(self, name, parameters):
        self.name = name
        self.par = parameters

    def __repr__(self):
        return 'currency' + str(self.name)


class CurrencyParameters:
    """
    Holds the initial parameters
    """
    def __init__(self, country, nominal_interest_rate, quantity):
        self.country = country
        self.nominal_interest_rate = nominal_interest_rate
        self.quantity = quantity
