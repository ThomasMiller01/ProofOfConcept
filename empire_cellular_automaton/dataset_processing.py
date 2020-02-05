import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import time


def people_distribution_map(data, file):
    plt_size_x = int(np.ceil(np.sqrt(len(data['data']))))
    plt_size_y = int(np.ceil(np.sqrt(len(data['data'])) - 0.5))
    fig, axs = plt.subplots(plt_size_x, plt_size_y, figsize=(10, 10))
    fig.suptitle("people distribution", fontsize=10)
    fig.tight_layout(pad=3.0)
    i = 0
    s_all = ()
    s_mapped_all = None
    for ax_s in axs:
        for ax in ax_s:
            if i < len(data['data']):
                gen = data['data'][i]
                minified_data = [y['colonies']['0']['people']
                                 for y in gen['data']]
                all_people_list = []
                for day in minified_data:
                    for person in day:
                        all_people_list.append((person['x'], person['y']))
                unique, counts = np.unique(np.asarray(
                    all_people_list), return_counts=True, axis=0)

                x, y = zip(*unique)

                if not s_all:
                    s_all = (counts.min(), counts.max())
                    s_mapped_all = np.interp(
                        counts, (s_all[0], s_all[1]), (0, 100))
                s_mapped = np.interp(
                    counts, (counts.min(), counts.max()), (0, 100))

                color_palett = [
                    '#d3ae1b', '#de6e3b', '#b54d47', '#8e321e', '#522a1a']

                color_ranges = np.arange(
                    s_mapped_all.min(), s_mapped_all.max(), (s_mapped_all.max() - s_mapped_all.min()) / len(color_palett))

                color_indices = [np.where(n < color_ranges)[0]
                                 for n in s_mapped]
                colors = [color_palett[c[0]] if c.size != 0 else color_palett[len(
                    color_palett) - 1] for c in color_indices]

                img = plt.imread("map.jpg")

                ax.scatter(x, y, s=s_mapped, c=colors)
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
                all_people_list = []
                for day in minified_data:
                    for person in day:
                        all_people_list.append(
                            [person['_id'], person['_disease']['kind'][0] if person['_disease'] != None else None])
                all_people_list = np.asarray(all_people_list)
                all_diseased_people_list = all_people_list[np.where(
                    all_people_list[:, 1] != None)]
                unique_all, counts_all = np.unique(
                    all_diseased_people_list[:, 1], return_counts=True)

                x = np.arange(0, counts_all.size)
                y = np.asarray(counts_all)

                ax.bar(x, y)
                ax.set_xticks(x)
                ax.set_yticks(y)
                ax.set_xticklabels(unique_all)
                ax.set(title="gen " + str(gen['gen']))
                i += 1
    plt.savefig(file)
    plt.close(fig=fig)


def strength_distribution_per_generation(data, file):
    plt_size_x = int(np.ceil(np.sqrt(len(data['data']))))
    plt_size_y = int(np.ceil(np.sqrt(len(data['data'])) - 0.5))
    fig, axs = plt.subplots(plt_size_x, plt_size_y, figsize=(10, 10))
    fig.tight_layout(pad=3.0)
    fig.suptitle("strength distribution", fontsize=12)
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
               c='r', linestyle=':', label='rT')
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
    start_all = time.time()
    print("------")
    print("saving " + dataset_name)
    file_name = './datasets/' + dataset_name

    print("loading data ...")
    start = time.time()
    # load data
    with open(file_name + '/' + dataset_name + '.json') as json_file:
        data = json.load(json_file)
    end = time.time()
    print("data loaded in " + str(round(end - start, 2)) + "s")
    print("***")

    start = time.time()
    print("saving pdfs ...")
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

    end = time.time()
    print("pdfs saved in " + str(round(end - start, 2)) + "s")
    print("***")
    print("saving pngs ...")
    start = time.time()

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
    end = time.time()
    print("pngs saved in " + str(round(end - start, 2)) + "s")
    print("***")
    end_all = time.time()
    print("- " + dataset_name + " saved")
    print("- time elapsed: " + str(round(end_all - start_all, 2)) + "s")
    print("------")


if __name__ == "__main__":
    for directory in os.listdir('./datasets'):
        if "example" not in directory:
            save_figs(directory)
    print("creating statistics done")
