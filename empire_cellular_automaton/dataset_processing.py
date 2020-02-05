import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os


def people_distribution_map(data, file):
    plt_size_x = int(np.ceil(np.sqrt(len(data['data']))))
    plt_size_y = int(np.ceil(np.sqrt(len(data['data'])) - 0.5))
    fig, axs = plt.subplots(plt_size_x, plt_size_y, figsize=(10, 10))
    fig.suptitle("people distribution", fontsize=10)
    fig.tight_layout(pad=3.0)
    i = 0
    for ax_s in axs:
        for ax in ax_s:
            if i < len(data['data']):
                print(str(i))
                gen = data['data'][i]
                minified_data = [y['colonies']['0']['people']
                                 for y in gen['data']]
                x_y_not_duplicated = []
                x_y_not_duplicated_data = []
                print("for loop 1")
                for day in minified_data:
                    for person in day:
                        x_y = (person['x'], person['y'])
                        index = np.where(np.asarray(
                            x_y_not_duplicated) == x_y)[0]
                        if index.size == 0:
                            x_y_not_duplicated.append(x_y)
                            x_y_not_duplicated_data.append(1)
                        else:
                            x_y_not_duplicated_data[index[0]] += 1

                x = []
                y = []
                print("for loop 2")
                for x_y in x_y_not_duplicated:
                    x.append(x_y[0])
                    y.append(x_y[1])

                s = np.asarray(x_y_not_duplicated_data)

                color_palett = [
                    '#d3ae1b', '#de6e3b', '#b54d47', '#8e321e', '#522a1a']

                color_ranges = np.arange(
                    s.min(), s.max(), (s.max() - s.min()) / len(color_palett))
                colorsDict = {1: 'y', 5: 'c', 10: 'b',
                              15: 'g', 20: 'm', 30: 'r', 50: 'k'}

                print("for loop 3")
                colors = []
                for n in s:
                    found = False
                    for color_range in color_ranges:
                        if n < color_range:
                            colors.append(
                                color_palett[np.where(color_ranges == color_range)[0][0]])
                            found = True
                            break
                    if not found:
                        colors.append(
                            color_palett[len(color_palett) - 1])

                img = plt.imread("map.jpg")

                ax.scatter(x, y, s=s, c=colors)
                ax_xlim = ax.get_xlim()
                ax_ylim = ax.get_ylim()
                ax.imshow(img, origin="lower")
                ax.set_xlim(ax_xlim)
                ax.set_ylim(ax_ylim[::-1])
                ax.set(title="gen " + str(gen['gen']))
                i += 1
    plt.savefig(file)
    plt.close(fig=fig)


def kind_of_disease_per_generation(data, file):
    plt_size_x = int(np.ceil(np.sqrt(len(data['data']))))
    plt_size_y = int(np.ceil(np.sqrt(len(data['data'])) - 0.5))
    fig, axs = plt.subplots(plt_size_x, plt_size_y, figsize=(10, 10))
    fig.suptitle("kind of disease", fontsize=16)
    fig.tight_layout(pad=3.0)
    i = 0
    for ax_s in axs:
        for ax in ax_s:
            if i < len(data['data']):
                gen = data['data'][i]
                minified_data = [y['colonies']['0']['people']
                                 for y in gen['data']]
                disease_num = {}
                diseased_people_ids = []
                for day in minified_data:
                    for person in day:
                        if person['_disease'] != None and np.where(np.asarray(diseased_people_ids) == (person['_id'], person['_disease']['kind'][0]))[0].size == 0:
                            diseased_people_ids.append(
                                (person['_id'], person['_disease']['kind'][0]))
                            if person['_disease']['kind'][0] not in disease_num:
                                disease_num[person['_disease']['kind'][0]] = 1
                            else:
                                disease_num[person['_disease']['kind'][0]] += 1

                y_list_data = []
                y_list_labels = []
                for kind in disease_num:
                    y_list_data.append(disease_num[kind])
                    y_list_labels.append(kind)
                x = np.arange(0, len(y_list_data))
                y = np.asarray(y_list_data)

                ax.bar(x, y)
                ax.set_xticks(x)
                ax.set_yticks(y)
                ax.set_xticklabels(y_list_labels)
                ax.set(title="gen " + str(gen['gen']))
                i += 1
    plt.savefig(file)
    plt.close(fig=fig)


def strength_distribution_per_generation(data, file):
    plt_size_x = int(np.ceil(np.sqrt(len(data['data']))))
    plt_size_y = int(np.ceil(np.sqrt(len(data['data'])) - 0.5))
    fig, axs = plt.subplots(plt_size_x, plt_size_y, figsize=(10, 10))
    fig.tight_layout(pad=3.0)
    fig.suptitle("strength distribution", fontsize=16)
    i = 0
    for ax_s in axs:
        for ax in ax_s:
            if i < len(data['data']):
                gen = data['data'][i]
                minified_data = gen['data'][len(
                    gen['data']) - 1]['colonies']['0']['people']
                x = np.arange(0, 100)
                y = np.zeros(100)
                for age in [a['_strength'] for a in minified_data]:
                    y[int(np.ceil(age)) - 1] += 1

                coeffs = np.polyfit(x, y, 3)
                poly_eqn = np.poly1d(coeffs)
                y_hat = poly_eqn(x)

                ax.plot(x, y)
                ax.plot(x, y_hat, label="average", c='r')
                ax.set(xlabel='strength', ylabel='people',
                       title="gen " + str(gen['gen']))
                ax.grid()
                i += 1
    plt.savefig(file)
    plt.close(fig=fig)


def age_distribution_per_generation(data, file):
    plt_size_x = int(np.ceil(np.sqrt(len(data['data']))))
    plt_size_y = int(np.ceil(np.sqrt(len(data['data'])) - 0.5))
    fig, axs = plt.subplots(plt_size_x, plt_size_y, figsize=(10, 10))
    fig.tight_layout(pad=3.0)
    fig.suptitle("age distribution", fontsize=16)
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
                    if age > 100:
                        age = 100
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
    plt.close(fig=fig)


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
    plt.close(fig=fig)


def avg_reproductionValue_over_time(data, file):
    fig, ax = plt.subplots()
    for gen in data['data']:
        minified_data = gen['data']
        x = np.arange(0, len(minified_data))
        y = np.asarray([np.average(
            [a['_reproductionValue'] for a in d['colonies']['0']['people']]) for d in minified_data])
        ax.plot(x, y, label=gen['gen'])
    ax.axhline(data['settings']['p_reproductionThreshold'],
               c='r', linestyle=':', label='reproductionThreshold')
    ax.set(xlabel='days', ylabel='reproductionValue',
           title='avg reproductionValue over time')
    ax.grid()
    plt.legend(loc="best", title="generation")
    plt.savefig(file)
    plt.close(fig=fig)


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
    plt.close(fig=fig)


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
    plt.close(fig=fig)


def save_figs(dataset_name):
    print("saving " + dataset_name + " ...")
    file_name = './datasets/' + dataset_name

    # load data
    with open(file_name + '/' + dataset_name + '.json') as json_file:
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
    age_distribution_per_generation(
        data, file_name + "/pdf/age_distribution_per_generation.pdf")
    strength_distribution_per_generation(
        data, file_name + "/pdf/strength_distribution_per_generation.pdf")
    kind_of_disease_per_generation(
        data, file_name + "/pdf/kind_of_disease.pdf")
    people_distribution_map(
        data, file_name + "/pdf/people_distribution_map.pdf")

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
    age_distribution_per_generation(
        data, file_name + "/png/age_distribution_per_generation.png")
    strength_distribution_per_generation(
        data, file_name + "/png/strength_distribution_per_generation.png")
    kind_of_disease_per_generation(
        data, file_name + "/png/kind_of_disease.png")
    people_distribution_map(
        data, file_name + "/png/people_distribution_map.png")


if __name__ == "__main__":
    # for directory in os.listdir('./datasets'):
    #     save_figs(directory)
    save_figs("example_dataset_06")
    print("creating statistics done")
