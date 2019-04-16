#!/usr/bin/env python2
# -*- coding: utf-8 -*-


class Underwriter:
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


class ExoAgentVariablesTime:
    """
    Holds the initial variables for the agents
    """
    def __init__(self, assets, currency, asset_demand, currency_demand):
        self.assets = assets  # The quantities of assets held
        self.currency = currency  # The quantities of currencies held
        self.asset_demand = [asset_demand]
        self.currency_demand = [currency_demand]


class ExoAgentParameters:
    """
    Holds the the agent parameters
    """
    def __init__(self, country):
        self.country = country


class CB_Variables:
    """Holds the inital variables for the central bank"""
    def __init__(self, assets, currency, asset_demand, currency_demand, asset_target):
        self.assets = assets # The quantities of assets held
        self.currency = currency # The quantities of currencies held
        self.asset_demand = asset_demand
        self.currency_demand = currency_demand
        self.asset_target = asset_target


class CB_VariablesTime:
    """Holds the inital variables for the central bank"""
    def __init__(self, assets, currency, asset_demand, currency_demand, asset_target):
        self.assets = assets # The quantities of assets held
        self.currency = currency # The quantities of currencies held
        self.asset_demand = asset_demand
        self.currency_demand = currency_demand
        self.asset_target = asset_target


class Central_Bank:
    """
    Class holding central bank properties
    """
    def __init__(self, variables, previous_variables, parameters):
        self.var = variables
        self.var_previous = previous_variables
        self.par = parameters
 
    def __repr__(self):
        return 'central_bank_' + str(self.par.country)


class FX_Interventionist:
    def __init__(self, variables):
        self.var = variables

    def __repr__(self):
        return 'fx_interventionist'



class FX_Interventionist_Variables:
    """Holds the inital variables for the central bank"""
    def __init__(self, asset_demand, currency, currency_demand):
        self.asset_demand = asset_demand
        self.currency = currency # The quantities of currencies held
        self.currency_demand = currency_demand
