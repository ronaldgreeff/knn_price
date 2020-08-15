import os
import csv

from models import DBWriter
from management import LocalFiles
from selenium_obj import Driver

if __name__ == '__main__':

    local_files = LocalFiles()
    db_write = DBWriter()
    script = 'inject.js'

    # try:
    #     crawler = Driver(script)
    #     src = 'data\\adorebeauty\\Cloud Nine Gift of Gold - Original Iron Reviews + Free Post.html'
    #     extract = crawler.process_file(src)

    #     for text in extract['texts']:
    #         print('{} {} {}'.format(
    #             text['bound']['calc']['normalisedTop'],
    #             text['bound']['calc']['normalisedVolume'],
    #             [t.encode('utf-8').strip() for t in text['text']],))

    # finally:
    #     crawler.quit(m="end run.")

    for url, src in local_files.yield_file_paths():

        try:
            crawler = Driver(script)
            extract = crawler.process_file(src)

            url = 'https://www.adorebeauty.com.au/cloud-nine-cloud-9/cloud-nine-gift-of-gold-original-iron-2018.html'
            src = 'C:\\Users\\User McUser\\Projects\\python\\knn_price\\project\\data\\adorebeauty\\Cloud Nine Gift of Gold - Original Iron Reviews + Free Post.html'

            db_write.store_page_extract(url=url, extract=extract)

            print(url)
            print(src)
            for text in extract['texts']:
                print('{:.2f} {:.2f} {}'.format(
                    ((text['bound']['calc']['normalisedTop']*100)),
                    ((text['bound']['calc']['normalisedVolume']*100)),
                    [t.encode('utf-8') for t in text['text']],))

            break

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