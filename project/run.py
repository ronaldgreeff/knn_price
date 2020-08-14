import os
import csv

from models import DBWriter
from management import LocalFiles
from selenium_obj import Driver

if __name__ == '__main__':

    # single_eg = {"adorebeauty": ["Cloud Nine Gift of Gold - Original Iron Reviews + Free Post.html"]}
    # src = os.path.join(os.getcwd(), 'data', 'adorebeauty', single_eg['adorebeauty'][0])
    local_files = LocalFiles()
    # temp_local_file = local_files.pages['adorebeauty'][0]
    script = 'inject.js'

    for i in local_files.yield_file_paths():
        print(i)

    # try:
    #     crawler = Driver(script)

    #             extract = crawler.process_file(src)

    # finally:
    #     crawler.quit(m="end run.")



    # crawler = Driver()
    # crawler.process_file()

    # dbw = DBWriter()


    # x = DataImport()

    # for i in x.get_local_page_paths():
    #     print(os.path.exists(i))

    # for folder in x.data:

    #     url_list = []
    #     with open(os.path.join(os.getcwd(), 'data', folder, 'urls.txt'), 'r') as url_file:
    #         url_list = url_file.readlines()

    #     file_list = os.listdir(os.path.join(os.getcwd(), 'data', folder))