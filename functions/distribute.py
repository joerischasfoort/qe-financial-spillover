import random
from bisect import bisect

""" Helper functions to assign funds to countries """

def distribute_options_equally(n_funds, list_options):
    """
    param: n_funds: integer of total number of funds to be assigned to a country
    param: list_options list of strings contains the countries
    returns: list of evenly distributed list of countries
    """
    funds = []
    for fund in range(n_funds):
        for i in range(len(list_options)):
            funds.append(list_options[i])

    return funds[:n_funds]


def ordered_list_of_countries(n_domestic, n_foreign):
    """
    Create list of shape ['domestic'...n & 'foreign'....n]
    :param n_domestic: number of domestic object
    :param n_foreign: number of foreign objects
    :return: list
    """
    return ['domestic' for x in range(n_domestic)] + ['foreign' for x in range(n_foreign)]


def weighted_choice(choices):
    """
    param: choices list of tuples with (Country, chance of getting country)
    returns: string of chosen country
    from https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
    """
    values, weights = zip(*choices)
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random.random() * total
    i = bisect(cum_weights, x)
    return values[i]

def split_equal(parts, value):
    """

    :param parts: number of parts the value will be split into
    :param value:  the value that needs to be divided by parts
    :return: list with equal distributed parts
    """
    value = float(value)
    return [1 * value / parts for i in range(1, parts + 1)]
