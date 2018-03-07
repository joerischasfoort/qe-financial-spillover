#!/usr/bin/env python2
# -*- coding: utf-8 -*-


class Underwriter():
    """Class holding underwriter properties"""
    def __init__(self, variables, previous_variables):
        self.var = variables
        self.var_previous = previous_variables
 
    def __repr__(self):
        return 'underwriter'
    

class ExoAgentVariables:
    """
    Holds the initial variables for the agents
    """
    def __init__(self, assets, currency, asset_demand, currency_demand):
        self.assets = assets # The quantities of assets held
        self.currency = currency # The quantities of currencies held
        self.asset_demand = asset_demand
        self.currency_demand = currency_demand
     

class ExoAgentParameters:
    """
    Holds the the agent parameters
    """
    def __init__(self, nationality):
        self.nationality = nationality


class Central_Bank():
    """
    Class holding central bank properties
    """
    def __init__(self, variables, previous_variables, parameters):
        self.var = variables
        self.var_previous = previous_variables
        self.par = parameters
 
    def __repr__(self):
        return 'central_bank_' + str(self.par.nationality)
