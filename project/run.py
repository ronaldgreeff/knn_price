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
        for url, vd, page in local_files.yield_file_paths():
            src = os.path.join(vd, page)

            extract = crawler.process_file(vd=vd, page=page, screenshot=True)
            # crawler.close()

            db_write.store_page_extract(url=url, extract=extract)

    finally:
        crawler.quit()
