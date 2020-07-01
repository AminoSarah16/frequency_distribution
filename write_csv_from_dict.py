import csv
import os
import configparser
import random


def main():
    replicate1_small = []
    replicate2_small = []
    replicate3_small = []
    replicate1_large = []
    replicate2_large = []
    replicate3_large = []

    for i in range(5):
        val = round(random.random(), 2)  # generates a sequence of random floats, where 2 specifies the number of decimal places
        replicate1_small.append(val)

    print(replicate1_small)

    test_dict = {"replicate1_small": replicate1_small, "replicate2_small": replicate2_small, "replicate3_small": replicate3_small}


    # sämtliche meiner Test was man mit so einem Dictionary alles machen kann
    key_list = test_dict.keys()
    print(test_dict)
    print(key_list)

    for key, value in test_dict.items():
        print(key)
    for values_in_list in test_dict.values():
       #mit einer list comprehension wird es als liste geprinted
       print([value for value in values_in_list])  #die eckige Klammer ist unendlich wichtig, weil sonst erzählt er irgendwas von generator object.

       #mit einer for loop wird jeder value separat geprinted
       for value in values_in_list:
           print(value)

        # print( for value in value)


    # MAIN learning from this test file:
    # save dictionnary as .csv with keys as row headers
    test_path = get_path('test-path')
    name = "test_table.csv"
    result = os.path.join(test_path, name)
    with open(result, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for keys, values_in_list in test_dict.items():
            writer.writerow([keys] + [value for value in values_in_list])
            # brauche diese list comprehension ("value for value..." als quasi zweite for loop) um über die einzelnen
            # Elemente der Liste, die in dem "value" vom key:value pair des dictionaries stecken zu iterieren und in je
            # eine neue column zu schreiben



def get_path(path):
    """
    Retrieves the paths from the .ini file
    """
    config = configparser.ConfigParser()
    config.read('filepath.ini')
    return config['general'][path]


if __name__ == '__main__':
    main()
