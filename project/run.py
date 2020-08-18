import os
import csv
import time

from models import DBWriter, DBReader
from management import LocalFiles
from selenium_obj import Driver
from pandas_obj import DataObj
from urllib.parse import urlparse, urlunparse

def get_filename_form_url(url):

    parsed_url = urlparse(url)
    netloc_split = parsed_url[1].split('.')
    vendor = netloc_split[1] if 'www' in netloc_split else netloc_split[0]
    temp = vendor + parsed_url[2]
    filename = ''.join([i for i in temp if i not in ('-', '/', 'a', 'e', 'i', 'o', 'u')])
    return filename

def web_data_to_db():

    local_files = LocalFiles()
    db_write = DBWriter()
    crawler = Driver('inject.js')

    # from web - using this as saving webpage first loses some of the styling

    urls = [
        'https://www.beautybay.com/p/beauty-bay/liquid-crystal-eyeshadow/tourmaline/',
        'https://www.beautybay.com/p/sample-beauty/the-painters-palette/',
        'https://www.beautybay.com/p/sugarpill-cosmetics/liquid-lip-color/',
        ]

    for url in urls:
        filename = get_filename_form_url(url)

        try:
            url, extract = crawler.get_page(url)
            crawler.save_screenshot(
                os.path.join(local_files.data_dir, 'screenshots', filename) )
            db_write = DBWriter()
            db_write.store_page_extract(url=url, extract=extract)
            local_files.add_url(vendor, url)
        finally:
            crawler.quit()

def local_data_to_db():

    try:
        for url, vd, page in local_files.yield_file_paths():
            src = os.path.join(dir, filename)
            extract = crawler.process_file(dir=dir, filename=filename)
            db_write.store_page_extract(url=url, extract=extract)
    finally:
        crawler.quit()

def db_to_memory():
    db_read = DBReader()
    data = DataObj()
    data.show()

if __name__ == '__main__':

    # m.local_data_to_db()
    db_to_memory()
