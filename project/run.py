import os
import csv

if __name__ == '__main__':
    x = DataImport()

    for i in x.get_local_page_paths():
        print(os.path.exists(i))


    # for folder in x.data:

    #     url_list = []
    #     with open(os.path.join(os.getcwd(), 'data', folder, 'urls.txt'), 'r') as url_file:
    #         url_list = url_file.readlines()

    #     file_list = os.listdir(os.path.join(os.getcwd(), 'data', folder))