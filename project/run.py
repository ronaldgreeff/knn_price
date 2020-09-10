import os
import csv
import time

from models import DBWriter, DBReader
from management import LocalFiles
from pandas_obj import DataObj
import helpers


def web_data_to_db():
    """ Load up file manager, db writer and crawler. Crawl urls. Quit crawler """

    # todo: shouldn't be here, move
    # Selenium always seems to load, even when not imported??
    from selenium_obj import Driver

    local_files = LocalFiles()
    db_write = DBWriter()
    crawler = Driver('inject.js')

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
    """ *Less preferred method*
    Load up file manager, db writer and crawler. Crawl folders. Quit crawler
    """
    # todo: shouldn't be here, move
    from selenium_obj import Driver

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
    # specify css keys to retrieve from database
    css_keys = ['color', 'font-size', 'font-weight', 'text-transform',
        # 'text-align', 'vertical-align', 'text-shadow', 'font-family',
        ]
    data = DataObj(css_keys=css_keys)
    data.get_dataframes([1,2,3,4,5])
    data.pre_process()


if __name__ == '__main__':

    # web_data_to_db()

    db_to_memory()
