import numpy as np

def creating_lists(var, funds, portfolios,currencies, environment,exogeneous_agents):
    output = {}
    if "prices" in var:
        output.update({"portfolios["+str(p)+"].var.price": [] for p in range(len(portfolios))})
    if "fx" in var:
        output.update({"environment.var.fx_rates.iloc[0,1]":[]})
    if "returns" in var:
        output.update({"funds["+str(f)+"].exp.returns[portfolios[" + str(a)+"]]": [] for f in range(len(funds)) for a in range(len(portfolios))})
        output.update({"funds["+str(f)+"].exp.returns[currencies[" + str(a)+"]]": [] for f in range(len(funds)) for a in range(len(currencies))})
    if "weights" in var:
        output.update({"funds["+str(f)+"].var.weights[portfolios[" + str(a)+"]]": [] for f in range(len(funds)) for a in range(len(portfolios))})
        output.update({"funds["+str(f)+"].var.weights[currencies[" + str(a)+"]]": [] for f in range(len(funds)) for a in range(len(currencies))})
    if "assets" in var:
        output.update({"funds["+str(f)+"].var.assets[portfolios[" + str(a)+"]]": [] for f in range(len(funds)) for a in range(len(portfolios))})
        output.update({"funds["+str(f)+"].var.currency[currencies[" + str(a)+"]]": [] for f in range(len(funds)) for a in range(len(currencies))})


    return output


def add_observations(lists, funds, portfolios,currencies, environment,exogeneous_agents):
    for l in lists:
        lists[l].append(eval(l))

    return lists


def relative_development(raw_data, benchmark):
    relative_data = {}
    for data in raw_data:
        relative_data.update({data:{}})
        for var in raw_data[data]:
            if var.split(".")[1]=="exp":
                params = [int(x) for x in var if x.isdigit()]
                
                relative_data[data].update({var: (np.array(raw_data[data][var]) - np.array(raw_data[benchmark][var]))/abs(np.array(raw_data[benchmark][var]))})
    return relative_data