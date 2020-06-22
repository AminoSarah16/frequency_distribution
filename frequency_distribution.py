import os
import configparser
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

#in µm²
SMALL_THRESHOLD = 0.01   # 0.01  100x100 nm  #0.1 for test data
MEDIUM_THRESHOLD = 0.04  #0.04  200x200 nm  #0.5 for test data
ROW_HEADERS = ('Small (<{})'.format(SMALL_THRESHOLD), 'Medium (<{})'.format(MEDIUM_THRESHOLD), 'Large')

def main():
    table_path = get_table_path()
    filename = "bax-cluster-areas_Sarah.csv"
    file = os.path.join(table_path, filename)
    # file = "test_table.csv"

    # size_thresholds = ["small clusters up to " + str(SMALL_THRESHOLD) + "µm²:", "medium clusters up to " + str(MEDIUM_THRESHOLD) + "µm²:", "large clusters larger than " + str(MEDIUM_THRESHOLD) + "µm²:"]
    # print(size_thresholds)

    frequency_table, area_distribution_table, column_headers = create_tables(file)

    # frequency_table.insert(0, size_thresholds)  ##TODO: row headers

    # frequency distribution table
    name = "frequency_table_{:.2f}_{:.2f}.csv".format(SMALL_THRESHOLD, MEDIUM_THRESHOLD)
    numpy_and_save(frequency_table, table_path, name, column_headers, ROW_HEADERS)

    # area table
    name = "area_distribution_table_{:.2f}_{:.2f}.csv".format(SMALL_THRESHOLD, MEDIUM_THRESHOLD)
    numpy_and_save(area_distribution_table, table_path, name, column_headers, ROW_HEADERS)


def get_table_path():
    """
    Retrieves the root path
    """
    config = configparser.ConfigParser()
    config.read('filepath.ini')
    return config['general']['table-path']


def create_tables(filename):
    # read in the table with Pandas package
    original_table = pd.read_csv(filename, delimiter=',')
    # print(table)
    frequency_table = []
    area_distribution_table = []
    headers = []
    for column in original_table:
        print("\n", column)

        #fügt der Headers Liste die Namen der Spalten des original files hinzu
        headers.append(column)

        # sum1 = len(table[column])  #dient nur zur Überprüfung ob ich alle Werte finde (vgl sum2)
        # aufdröseln der values in einer column in die drei Clustergrößen durch list comprehension
        # macht drei individuelle Listen draus
        small_clusters = [value for value in original_table[column] if value <= SMALL_THRESHOLD]
        medium_clusters = [value for value in original_table[column] if SMALL_THRESHOLD < value <= MEDIUM_THRESHOLD]
        large_clusters = [value for value in original_table[column] if value > MEDIUM_THRESHOLD]

        print(small_clusters, "\n", medium_clusters, "\n", large_clusters)

        # rechnet die Häufigkeiten aus, mit der ein Cluster vorkommt
        small_cluster_number = len(small_clusters)
        medium_cluster_number = len(medium_clusters)
        large_cluster_number = len(large_clusters)

        # und fügt sie einer neuen Liste hinzu
        frequency_row = []
        frequency_row.extend((small_cluster_number, medium_cluster_number, large_cluster_number))
        print("each category contains this many clusters:")
        print(frequency_row)

        # sum2 = small_cluster_sum + medium_cluster_sum + large_cluster_sum #dient nur zur Überprüfung ob ich alle
        # Werte finde (vgl sum1)

        # print("All values found: ", sum1==sum2)  #dient nur zur Überprüfung ob ich alle Werte finde (vgl sum1)

        frequency_table.append(frequency_row)

        # rechent die absolute Fläche aus, die von dieser Clusterkategorie eingenommen wird
        small_cluster_area = sum(small_clusters)
        medium_cluster_area = sum(medium_clusters)
        large_cluster_area = sum(large_clusters)

        print("cluster areas are: ")
        print(small_cluster_area, medium_cluster_area, large_cluster_area)

        area_row = []
        # TODO cluster areas müssen auf Zellfläche normiert werden
        # areas = np.array((small_cluster_area, medium_cluster_area, large_cluster_area))
        # area_row.extend(areas / np.sum(areas))
        area_row.extend((small_cluster_area, medium_cluster_area, large_cluster_area))
        print(area_row)

        area_distribution_table.append(area_row)

    print("\n", frequency_table)
    print("\n", area_distribution_table)

    # macht aus der Headers liste einen String mit Kommas
    print("\n", headers)
    #headers_str = ','.join(headers)
    #print(headers_str)

    return frequency_table, area_distribution_table, headers


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

    # jetzt mit csv package
    with open(result, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([''] + column_headers)
        for i in range(len(row_headers)):
            writer.writerow([row_headers[i]] + [value for value in transposed[i, :]])


if __name__ == '__main__':
    main()