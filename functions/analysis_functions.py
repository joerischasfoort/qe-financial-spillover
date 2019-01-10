import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc


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
    if "default_prob" in var:
        output.update({"funds[0].exp.default_rates[portfolios[" + str(a)+"]]": [] for a in range(len(portfolios))})
    if "covariance" in var:
        output.update({"funds[0].var.covariance_matrix.iloc["+str(a)+","+str(b)+"]": [] for a in range(6) for b in range(6)})
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
            relative_data[data].update({var: (np.array(raw_data[data][var]) - np.array(raw_data[benchmark][var]))})
    return relative_data


def relative_development2(raw_data, benchmark):
    relative_data = {}
    for data in raw_data:
        relative_data.update({data:{}})
        for var in raw_data[data]:
            relative_data[data].update({var: (np.array(raw_data[data][var]) - np.array(raw_data[benchmark][var]))})
    return relative_data



def compute_averages(input_data,benchmark, ordered_var_list, t_range):
    data_means = {}
    data_5p = {}
    data_95p = {}
    for var in input_data[benchmark]:
        data_means.update({var:[]})
        data_5p.update({var:[]})
        data_95p.update({var:[]})
        for data in ordered_var_list:
            data_means[var].append(np.mean(np.array(input_data[data][var])[t_range]))
            data_5p[var].append(np.percentile(np.array(input_data[data][var])[t_range],5))
            data_95p[var].append(np.percentile(np.array(input_data[data][var])[t_range],95))

    return data_means, data_5p, data_95p


def compute_MCaverages(input_data, seed_list):
    data_means = {}
    data_5p = {}
    data_95p = {}
    for var in input_data[seed_list[0]]:
        data_means.update({var:[]})
        data_5p.update({var: []})
        data_95p.update({var: []})
        for i in range(len(input_data[seed_list[0]][var])):
            data_means[var].append(np.mean(np.array([input_data[seed][var][i] for seed in seed_list])))
            data_5p[var].append(np.percentile(np.array([input_data[seed][var][i] for seed in seed_list]),5))
            data_95p[var].append(np.percentile(np.array([input_data[seed][var][i] for seed in seed_list]),95))

    return data_means, data_5p, data_95p



def plot_conf(var,data_mean, data_p5, data_p95, ordered_var_list,x_factor,y_factor, location, name, saving):
    rc('text', usetex=True)

    fig, ax = plt.subplots()
    x = np.array(ordered_var_list)*x_factor
    y_mean = np.array(data_mean[var])*y_factor
    ax.plot(x, y_mean, "-b", label='a')

    y_p5 = np.array(data_p5[var]) * y_factor
    ax.plot(x, y_p5, linestyle='--', color='xkcd:grey')
    y_p95 = np.array(data_p95[var]) * y_factor
    ax.plot(x, y_p95, linestyle='--', color='xkcd:grey', label = "c")

    plt.xlabel("x")
    plt.ylabel('y')
    ax.legend(loc=location, frameon=False, labelspacing=1.5)
    if saving == 1:
        plt.savefig(name+'.eps', format="eps")

def compute_difference(data1, data2):
    result = {}
    for var1 in data1:
        for var2 in data2:
            if var1.split("_")[-1] == var2.split("_")[-1]:
                result.update({var1.split("_")[-1]:{}})
                for d in data1[var1]:
                    result[var1.split("_")[-1]].update({d: np.array(data1[var1][d])-np.array(data2[var2][d])})

    return result


def format_data_for_regression(new_data):
    data_frame = pd.DataFrame({'QE':[], 'seed':[]})
    for qe in new_data:
        for var in new_data[qe]:
            for seed in new_data[qe][var]:
                data_frame.update