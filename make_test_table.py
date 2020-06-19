import random
import numpy as np

COLUMNS = 4
ROWS = 30

def main():
    # eine tabelle ist nichts anderes als ne Liste (columns) von Listen (rows)
    test_table = []

    for i in range(ROWS):
        row = []
        for j in range(COLUMNS):
            val = round(random.random(), 2)  #generates a sequence of random floats, where 2 specifies the number of decimal places
            row.append(val)

        test_table.append(row)

    print(test_table)

    np_table = np.asarray(test_table)
    print(np_table)

    # generate string of list for headers
    headers = []
    for k in range(COLUMNS):
        header = "column" + str(k + 1)
        headers.append(header)
    print("\n", headers)
    headers_str = ','.join(headers)
    print(headers_str)

    #save the table and give it headers
    np.savetxt("test_table.csv", np_table, delimiter=',', header=headers_str, fmt='%f', comments='')  #fmt (format) specifies how the values should be represented eg. f means decimal floating point


if __name__ == '__main__':
    main()
