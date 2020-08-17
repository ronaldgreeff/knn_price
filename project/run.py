import os
import csv
import time

from models import DBWriter, DBReader
from management import LocalFiles
from selenium_obj import Driver
from pandas_obj import DataObj

class Main():

    def local_data_to_db(self):

        local_files = LocalFiles()
        db_write = DBWriter()
        crawler = Driver('inject.js')

        try:
            for url, vd, page in local_files.yield_file_paths():
                src = os.path.join(vd, page)
                extract = crawler.process_file(vd=vd, page=page, screenshot=True)

                db_write.store_page_extract(url=url, extract=extract)

        finally:
            crawler.quit()

    def db_to_memory(self):
        db_read = DBReader()
        data = DataObj()
        print(data.df0)

if __name__ == '__main__':

    m = Main()
    # m.local_data_to_db()
    m.db_to_memory()
