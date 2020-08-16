import os
import csv
import time

from models import DBWriter
from management import LocalFiles
from selenium_obj import Driver

if __name__ == '__main__':

    local_files = LocalFiles()
    db_write = DBWriter()
    script = 'inject.js'

    crawler = Driver(script)

    try:
        for url, src in local_files.yield_file_paths():
            print(src)

            extract = crawler.process_file(src)
            # crawler.close()

            db_write.store_page_extract(url=url, extract=extract)

    finally:
        crawler.quit()