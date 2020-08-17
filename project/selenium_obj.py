import os
import csv
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class Driver_Config():
    """ For Driver cconsistency, set things like
    headless state, browser driver and window size """

    options = Options()
    options.headless=True
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1920, 1080)
    # driver.maximize_window()

class Driver(Driver_Config):
    """ Main driver for navigating to webpage and interacting with it """

    def __init__(self, script):
        """ Initiate driver and load script """
        self.driver = Driver_Config.driver
        self.script = open(script).read()

    def quit(self, m=None):
        """ Quit the driver. Print a message if provided """
        if m:
            print('{}'.format(m))
        self.driver.quit()

    def extract_from_document(document):
        """ Navigate to URL or local file (document), inject script, return
        extract, catch any exceptions """
        try:
            self.driver.get(document)
        except Exception as e:
            self.quit(m='FAILED EXTRACT: {}'.format(e))

        extract = self.driver.execute_script(self.script)
        return extract

    def process_url(self, url):
        """ Extract from a url """
        # TODO: process url for vendor and file name
        return self.extract_from_document(url)

    def process_file(self, vd, page, screenshot=False):
        """ Extract from local file """

        local_file = 'file://{}'.format( os.path.join(vd, page) )
        extract = self.extract_from_document(local_file)

        if screenshot:
            f = page.split('.')[0]
            n = f + '.jpg'
            sd = os.path.join('data', '_screenshots', n)

            self.driver.save_screenshot(sd)

        return extract
