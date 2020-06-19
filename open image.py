from skimage.io import imread
import matplotlib.pyplot as plt
import os
import configparser


def main():
    root_path = get_root_path()
    filename = "IF29_spl20_U2OS-DKO_6hEx_14hAct_pcDNA-Bax-wt_cytC-AF488_Tom20-AF594_Bax-SR_cl1_RingsClustersExpControl Ch2 {2}0contr_enh.jpg"
    file_path = os.path.join(root_path, filename)

    image = imread(file_path)

    plt.imshow(image, cmap="gray")
    plt.show()


def get_root_path():
    """
    Retrieves the root path
    """
    config = configparser.ConfigParser()
    config.read('filepath.ini')
    return config['general']['root-path']

if __name__ == '__main__':
    main()