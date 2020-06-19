import os
import configparser
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#in µm²
SMALL_THRESHOLD = 0.1   # 0.01  100x100 nm  #0.1 for test data
MEDIUM_THRESHOLD = 0.5  #0.04  200x200 nm  #0.5 for test data

def main():
    table_path = get_table_path()
    filename = "bax-cluster-areas_Sarah.csv"
    # file = os.path.join(table_path, filename)
    file = "test_table.csv"


    #print(filepath)

    size_thresholds = ["small clusters up to " + str(SMALL_THRESHOLD) + "µm²:", "medium clusters up to " + str(MEDIUM_THRESHOLD) + "µm²:", "large clusters larger than " + str(MEDIUM_THRESHOLD) + "µm²:"]
    print(size_thresholds)

    frequency_table, headers_str = create_frequency_table(file)

    # frequency_table.insert(0, size_thresholds)  ##TODO: row headers

    np_table = np.asarray(frequency_table)
    print("\n", np_table)

    transposed = np.transpose(np_table)
    print("\n", transposed)


    # save the table and give it headers
    np.savetxt("frequency_table.csv", transposed, delimiter=',', header=headers_str, fmt='%f',
    comments='')  # fmt (format) specifies how the values should be represented eg. f means decimal floating point


def create_frequency_table(filename):
    # read in the table with Pandas package
    original_table = pd.read_csv(filename, delimiter=',')
    # print(table)
    frequency_table = []
    headers = []
    for column in original_table:
        print("\n", column)
        headers.append(column)

        # sum1 = len(table[column])  #dient nur zur Überprüfung ob ich alle Werte finde (vgl sum2)
        # aufdröseln der values in einer column in die drei Clustergrößen durch list comprehension
        # macht drei individuelle Listen draus
        small_clusters = [value for value in original_table[column] if value <= SMALL_THRESHOLD]
        medium_clusters = [value for value in original_table[column] if SMALL_THRESHOLD < value <= MEDIUM_THRESHOLD]
        large_clusters = [value for value in original_table[column] if value > MEDIUM_THRESHOLD]

        print(small_clusters, "\n", medium_clusters, "\n", large_clusters)

        # rechnet die Häufigkeiten aus, mit der ein Cluster vorkommt
        small_cluster_sum = len(small_clusters)
        medium_cluster_sum = len(medium_clusters)
        large_cluster_sum = len(large_clusters)

        # und fügt sie einer neuen Liste hinzu
        row = []
        row.extend((small_cluster_sum, medium_cluster_sum, large_cluster_sum))
        print(row)

        # sum2 = small_cluster_sum + medium_cluster_sum + large_cluster_sum #dient nur zur Überprüfung ob ich alle
        # Werte finde (vgl sum1)

        # print("All values found: ", sum1==sum2)  #dient nur zur Überprüfung ob ich alle Werte finde (vgl sum1)

        frequency_table.append(row)

    print("\n", frequency_table)

    print("\n", headers)
    headers_str = ','.join(headers)
    print(headers_str)

    return frequency_table, headers_str


def get_table_path():
    """
    Retrieves the root path
    """
    config = configparser.ConfigParser()
    config.read('filepath.ini')
    return config['general']['table-path']


if __name__ == '__main__':
    main()