import os
import csv
import time

from models import DBWriter, DBReader
from management import LocalFiles
from selenium_obj import Driver
from pandas_obj import DataObj
import helpers


def web_data_to_db():

    local_files = LocalFiles()
    db_write = DBWriter()
    crawler = Driver('inject.js')

    # from web - using this as saving webpage first loses some of the styling

    try:
        for url in local_files.init_urls:
            vendor, filename = helpers.get_filename_from_url(url)
            extract = crawler.get_page(url)
            screenshot = os.path.join(
                local_files.data_dir, '_screenshots', (filename+'.png'))
            crawler.save_screenshot(screenshot)
            db_write.store_page_extract(url=url, extract=extract)
    finally:
        crawler.quit()

def local_data_to_db():

    local_files = LocalFiles()
    db_write = DBWriter()
    crawler = Driver('inject.js')

    try:
        for url, dir, filename in local_files.yield_file_paths():

            src = os.path.join(dir, filename)
            extract = crawler.process_file(dir=dir, filename=filename)
            screenshot = os.path.join(
                local_files.data_dir, '_screenshots', (filename+'.png'))
            crawler.save_screenshot(screenshot)
            db_write.store_page_extract(url=url, extract=extract)
    finally:
        crawler.quit()

def db_to_memory():
    db_read = DBReader()
    data = DataObj()
    data.show()

if __name__ == '__main__':

    # local_data_to_db()
    web_data_to_db()
    # db_to_memory()
