import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os


def population_pyramid_per_generation(data, file):
    plt_size_x = int(np.ceil((len(data['data']) / 2) - 0.5))
    plt_size_y = int(np.ceil(len(data['data']) / 2))
    fig, axs = plt.subplots(plt_size_x, plt_size_y, figsize=(10, 10), dpi=300)
    fig.tight_layout(pad=3.0)
    i = 0
    for ax_s in axs:
        for ax in ax_s:
            if i < len(data['data']):
                gen = data['data'][i]
                minified_data = gen['data'][len(
                    gen['data']) - 1]['colonies']['0']['people']
                x = np.arange(0, 100)
                y = np.zeros(100)
                for age in [a['_age'] for a in minified_data]:
                    y[int(np.ceil(age)) - 1] += 1

                coeffs = np.polyfit(x, y, 3)
                poly_eqn = np.poly1d(coeffs)
                y_hat = poly_eqn(x)

                ax.plot(x, y)
                ax.plot(x, y_hat, label="average", c='r')
                ax.set(xlabel='age', ylabel='people',
                       title="gen " + str(gen['gen']))
                ax.grid()
                i += 1
    plt.savefig(file)


def disease_over_time(data, file):
    fig, ax = plt.subplots()
    for gen in data['data']:
        minified_data = gen['data']
        x = np.arange(0, len(minified_data))
        y = np.asarray([np.sum(
            [1 if a['_disease'] else 0 for a in d['colonies']['0']['people']]) for d in minified_data])
        ax.plot(x, y, label=gen['gen'])
    ax.set(xlabel='days', ylabel='disease',
           title='disease over time')
    ax.grid()
    plt.legend(loc="best", title="generation")
    plt.savefig(file)


def avg_reproductionValue_over_time(data, file):
    fig, ax = plt.subplots()
    for gen in data['data']:
        minified_data = gen['data']
        x = np.arange(0, len(minified_data))
        y = np.asarray([np.average(
            [a['_reproductionValue'] for a in d['colonies']['0']['people']]) for d in minified_data])
        ax.plot(x, y, label=gen['gen'])
    ax.set(xlabel='days', ylabel='reproductionValue',
           title='avg reproductionValue over time')
    ax.grid()
    plt.legend(loc="best", title="generation")
    plt.savefig(file)


def avg_age_over_time(data, file):
    fig, ax = plt.subplots()
    for gen in data['data']:
        minified_data = gen['data']
        x = np.arange(0, len(minified_data))
        y = np.asarray([np.average(
            [a['_age'] for a in d['colonies']['0']['people']]) for d in minified_data])
        ax.plot(x, y, label=gen['gen'])
    ax.set(xlabel='days', ylabel='age',
           title='avg age over time')
    ax.grid()
    plt.legend(loc="best", title="generation")
    plt.savefig(file)


def population_over_time(data, file):
    fig, ax = plt.subplots()
    for gen in data['data']:
        minified_data = gen['data']
        x = np.arange(0, len(minified_data))
        y = np.asarray([len(d['colonies']['0']['people'])
                        for d in minified_data])
        ax.plot(x, y, label=gen['gen'])
    ax.set(xlabel='days', ylabel='population',
           title='population over time')
    ax.grid()
    plt.legend(loc="best", title="generation")
    plt.savefig(file)


if __name__ == "__main__":
    dataset_name = "dataset_02"

    file_name = 'statistics/' + dataset_name

    # load data
    with open(file_name + '/data.json') as json_file:
        data = json.load(json_file)

    # save as pdf
    try:
        os.mkdir(file_name + "/pdf")
    except:
        pass

    population_over_time(data, file_name + "/pdf/population_over_time.pdf")
    avg_age_over_time(data, file_name + "/pdf/avg_age_over_time.pdf")
    avg_reproductionValue_over_time(
        data, file_name + "/pdf/avg_reproductionValue_over_time.pdf")
    disease_over_time(data, file_name + "/pdf/disease_over_time.pdf")
    population_pyramid_per_generation(
        data, file_name + "/pdf/population_pyramid_per_generation.pdf")

    # save as png
    try:
        os.mkdir(file_name + "/png")
    except:
        pass

    population_over_time(data, file_name + "/png/population_over_time.png")
    avg_age_over_time(data, file_name + "/png/avg_age_over_time.png")
    avg_reproductionValue_over_time(
        data, file_name + "/png/avg_reproductionValue_over_time.png")
    disease_over_time(data, file_name + "/png/disease_over_time.png")
    population_pyramid_per_generation(
        data, file_name + "/png/population_pyramid_per_generation.png")
