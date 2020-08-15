import os
import csv

from models import DBWriter
from management import LocalFiles
from selenium_obj import Driver

if __name__ == '__main__':

    local_files = LocalFiles()
    # local_files.get_local_pages()

    for i in local_files.yield_file_paths():
        pass

    script = 'inject.js'

    src = "C:\\Users\\User McUser\\Projects\\python\\knn_price\\project\\data\\adorebeauty\\Cloud Nine Gift of Gold - Original Iron Reviews + Free Post.html"
    try:
        crawler = Driver(script)
        extract = crawler.process_file(src)

        texts = extract['texts']
        for t in texts:
            h = t['text']
            for x in h:
                print(x.encode('utf-8'))


    finally:
        crawler.quit(m="end run.")



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