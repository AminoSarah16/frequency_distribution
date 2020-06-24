import os
import configparser
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

# in µm²
SMALL_THRESHOLD = 0.01   # 0.01  100x100 nm  #0.1 for test data
MEDIUM_THRESHOLD = 0.04  #0.04  200x200 nm  #0.5 for test data

def main():
    result_path = get_path('result-path')
    print(result_path)
    bax_structures_path = get_path('bax-structures')
    print(bax_structures_path)
    root_path = (get_path('root-path'))
    # filename = "bax-cluster-areas_Sarah.csv"
    # file = os.path.join(root_path, filename)

    # for testing purposes
    # file = "test_table.csv"

    frequency_table = []
    area_table = []
    column_headers = []
    # counter = 0   # just for testing the loop
    for filename in sorted(os.listdir(bax_structures_path)):  #sorted() makes that it loops over the files in the folder sorted
        if filename.endswith("cluster-areas.csv"):
            column_header = get_column_headers(filename)
            column_headers.append(column_header)
            # counter += 1  # just for testing the loop
            file = os.path.join(bax_structures_path, filename)
            print(file)
            total_cluster_number, total_bax_area, relative_frequency, relative_area = calculate_relative_frequencies_and_areas(file)
            print("The total cluster number in this cell is {} and the total area this makes is {} µm².".format(total_cluster_number, total_bax_area))
            print("Each category contains {} % of all the clusters and makes up {} % of the total cluster area".format(relative_frequency, relative_area))


            # frequency distribution table
            row_headers = ('Small (x <= {})'.format(SMALL_THRESHOLD),
                           'Medium ({} < x <= {})'.format(SMALL_THRESHOLD, MEDIUM_THRESHOLD),
                           'Large ({} < x)'.format(MEDIUM_THRESHOLD), 'total cluster number')

            frequency_column = relative_frequency + [total_cluster_number]
            frequency_table.append(frequency_column)
            print(frequency_table)
            name = "table_of_frequencies_{:.2f}_{:.2f}.csv".format(SMALL_THRESHOLD, MEDIUM_THRESHOLD)
            numpy_and_save(frequency_table, result_path, name, column_headers, row_headers)

            # area table
            row_headers = ('Small (x <= {})'.format(SMALL_THRESHOLD),
                           'Medium ({} < x <= {})'.format(SMALL_THRESHOLD, MEDIUM_THRESHOLD),
                           'Large ({} < x)'.format(MEDIUM_THRESHOLD), 'total Bax area')

            area_column = relative_area + [total_bax_area]
            area_table.append(area_column)
            print(area_table)
            name = "table_of_areas_{:.2f}_{:.2f}.csv".format(SMALL_THRESHOLD, MEDIUM_THRESHOLD)
            numpy_and_save(area_table, result_path, name, column_headers, row_headers)

            # if counter == 2:  # just for testing the loop
            #     break


def get_path(path):
    """
    Retrieves the paths from the .ini file
    """
    config = configparser.ConfigParser()
    config.read('filepath.ini')
    return config['general'][path]


def get_condition(file):
    if 'Bax-wt' in file:
        return 'Bax_wt'
    if 'Bax-63-65A' in file:
        return 'Bax_63_65A'
    if 'Bax-H5i' in file:
        return 'Bax_H5i'
    if 'Bax-BH3i' in file:
        return 'Bax_BH3i'
    raise RuntimeError('Unknown condition in {}'.format(file))


def get_replicate(file):
    if 'IF29_' in file or 'IF40_' in file:
        return 'replicate1'
    if 'IF36_' in file:
        return 'replicate2'
    if 'IF41.2_' in file or 'IF41_' in file:
        return 'replicate3'
    raise RuntimeError('Unknown replicate in {}'.format(file))


def get_cell(filename):
    split = filename.split("-SR_")
    cell = split[1][0:-18]
    return cell


def get_column_headers(filename):
    condition = get_condition(filename)
    replicate = get_replicate(filename)
    cell = get_cell(filename)
    column_header = condition + '_' + replicate + '_' + cell
    return column_header


def calculate_relative_frequencies_and_areas(filename):
    # read in the table with Pandas package
    original_table = pd.read_csv(filename, header=None, delimiter=',')
    # print(original_table)

    for column in original_table:

        all_clusters = [value for value in original_table[column]]
        total_cluster_number = len(all_clusters)
        total_bax_area = sum(all_clusters)
        # print("The total cluster number in this cell is {} and the total area this makes is {} µm².".format(total_cluster_number, total_bax_area))

        small_clusters = [value for value in original_table[column] if value <= SMALL_THRESHOLD]
        medium_clusters = [value for value in original_table[column] if SMALL_THRESHOLD < value <= MEDIUM_THRESHOLD]
        large_clusters = [value for value in original_table[column] if value > MEDIUM_THRESHOLD]

        # print(small_clusters, "\n", medium_clusters, "\n", large_clusters)

        # rechnet die relativen Häufigkeiten aus, mit der eine Cluster-Kategorie vorkommt
        small_cluster_number = round(len(small_clusters)/total_cluster_number*100, 2)
        medium_cluster_number = round(len(medium_clusters)/total_cluster_number*100, 2)
        large_cluster_number = round(len(large_clusters)/total_cluster_number*100, 2)

        # und fügt sie einer neuen Liste hinzu
        relative_frequency = []
        relative_frequency.extend((small_cluster_number, medium_cluster_number, large_cluster_number))
        # print("Each category contains this many percent of all clusters:")
        # print(relative_frequency)

        # rechent die relative Fläche aus, die von dieser Clusterkategorie eingenommen wird
        small_cluster_area = round(sum(small_clusters)/total_bax_area*100, 2)
        medium_cluster_area = round(sum(medium_clusters)/total_bax_area*100, 2)
        large_cluster_area = round(sum(large_clusters)/total_bax_area*100, 2)

        relative_area = []
        relative_area.extend((small_cluster_area, medium_cluster_area, large_cluster_area))
        # print("Each category makes up this many percent of the total cluster area: ")
        # print(relative_area)

        return total_cluster_number, total_bax_area, relative_frequency, relative_area


def numpy_and_save(input_table, table_path, name, column_headers, row_headers):
    # transforms table to numpy array
    np_table = np.asarray(input_table)
    print("\n", np_table)
    # need to transpose because want replicates as columns
    transposed = np.transpose(np_table)
    print("\n", transposed)

    if len(column_headers) != transposed.shape[1]:
        raise RuntimeError('Anzahl der Spalten der Daten ungleich der Anzahl der Spaltennamen')
    if len(row_headers) != transposed.shape[0]:
        raise RuntimeError('Zeilen in Daten ungleich Anzahl der Zeilennamen')

    result = os.path.join(table_path, name)

    # mit csv package
    with open(result, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([''] + column_headers)  # [''] macht die erste Zelle leer
        for i in range(len(row_headers)):
            writer.writerow([row_headers[i]] + [value for value in transposed[i, :]]) # schreibt Zeile für Zeile wobei die erste Spalte mit den Headers gefüllt wird und die restlichen Zellen dann mit den Werten


if __name__ == '__main__':
    main()