import os
import configparser
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

# in µm²
SMALL_THRESHOLD = 0.01   # 0.01  100x100 nm  #0.1 for test data
MEDIUM_THRESHOLD = 0.04  #0.04  200x200 nm  #0.5 for test data
ROW_HEADERS = ('Small (x <= {})'.format(SMALL_THRESHOLD), 'Medium ({} < x <= {})'.format(SMALL_THRESHOLD, MEDIUM_THRESHOLD), 'Large ({} < x)'.format(MEDIUM_THRESHOLD))

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

    for filename in os.listdir(bax_structures_path):
        if filename.endswith("cluster-areas.csv"):
            file = os.path.join(bax_structures_path, filename)
            print(file)
            relative_frequency, relative_area = calculate_relative_frequencies_and_areas(file)
            # frequency_table, area_distribution_table = create_tables(file)
            #
            # # frequency distribution table
            # name = "table_of_frequencies_{:.2f}_{:.2f}.csv".format(SMALL_THRESHOLD, MEDIUM_THRESHOLD)
            # numpy_and_save(frequency_table, result_path, name, column_headers, ROW_HEADERS)
            #
            # # area table
            # name = "table_of_areas_{:.2f}_{:.2f}.csv".format(SMALL_THRESHOLD, MEDIUM_THRESHOLD)
            # numpy_and_save(area_distribution_table, result_path, name, column_headers, ROW_HEADERS)

            break

def get_path(path):
    """
    Retrieves the paths from the .ini file
    """
    config = configparser.ConfigParser()
    config.read('filepath.ini')
    return config['general'][path]


def calculate_relative_frequencies_and_areas(filename):
    # read in the table with Pandas package
    original_table = pd.read_csv(filename, header=None, delimiter=',')
    print(original_table)

    for column in original_table:

        all_clusters = [value for value in original_table[column]]
        total_cluster_number = len(all_clusters)
        total_bax_area = sum(all_clusters)
        print("The total cluster number in this cell is {} and the total area this makes is {} µm².".format(total_cluster_number, total_bax_area))

        small_clusters = [value for value in original_table[column] if value <= SMALL_THRESHOLD]
        medium_clusters = [value for value in original_table[column] if SMALL_THRESHOLD < value <= MEDIUM_THRESHOLD]
        large_clusters = [value for value in original_table[column] if value > MEDIUM_THRESHOLD]

        print(small_clusters, "\n", medium_clusters, "\n", large_clusters)

        # rechnet die relativen Häufigkeiten aus, mit der eine Cluster-Kategorie vorkommt
        small_cluster_number = len(small_clusters)/total_cluster_number*100
        medium_cluster_number = len(medium_clusters)/total_cluster_number*100
        large_cluster_number = len(large_clusters)/total_cluster_number*100

        # und fügt sie einer neuen Liste hinzu
        relative_frequency = []
        relative_frequency.extend((small_cluster_number, medium_cluster_number, large_cluster_number))
        print("Each category contains this many percent of all clusters:")
        print(relative_frequency)

        # rechent die relative Fläche aus, die von dieser Clusterkategorie eingenommen wird
        small_cluster_area = sum(small_clusters)/total_bax_area*100
        medium_cluster_area = sum(medium_clusters)/total_bax_area*100
        large_cluster_area = sum(large_clusters)/total_bax_area*100

        relative_area = []
        relative_area.extend((small_cluster_area, medium_cluster_area, large_cluster_area))
        print("Each category makes up this many percent of the total cluster area: ")
        print(relative_area)

        return relative_frequency, relative_area


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

    # np.savetxt(result, transposed, delimiter=',', header=headers_str, fmt='%f',
    # comments='')  # fmt (format) specifies how the values should be represented eg. f means decimal floating point

    # jetzt mit csv package, weils mehr kann als das savetxt dingens
    with open(result, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([''] + column_headers)  # [''] macht die erste Zelle leer
        for i in range(len(row_headers)):
            writer.writerow([row_headers[i]] + [value for value in transposed[i, :]]) # schreibt Zeile für Zeile wobei die erste Spalte mit den Headers gefüllt wird und die restlichen Zellen dann mit den Werten


if __name__ == '__main__':
    main()