import os
import configparser
import pandas as pd


def main():
    # table_path = get_table_path()
    # filename = "bax-cluster-areas_Sarah.csv"
    filename = "test_table.csv"
    # file_path = os.path.join(table_path, filename)

    # print(file_path)

    #read in the table with Pandas package
    table = pd.read_csv(filename, delimiter=',')
    print(table)

    print(table["column1"])  #prints the whole specified column
    print(table["column1"][0])  #access a specified row in the specified column

    for values in table["column1"]: #iterates over all rows in the specified column
        print(values)


def get_table_path():
    """
    Retrieves the root path
    """
    config = configparser.ConfigParser()
    config.read('filepath.ini')
    return config['general']['table-path']


if __name__ == '__main__':
    main()