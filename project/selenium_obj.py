import os
import csv
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class Driver_Config():

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    driver.set_window_size(1920, 1080)

# firefox not loading beautybay
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# class Driver_Config():
#     """ For Driver consistency, set things like
#     headless state, browser driver and window size """
#
#     ff_profile = webdriver.FirefoxProfile()
#     ff_profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0")
#
#     gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
#     binary = FirefoxBinary(r'C:\Program Files\Firefox Developer Edition\firefox.exe')
#
#     options = Options()
#     options.headless=False
#
#     driver = webdriver.Firefox(
#         firefox_binary=binary,
#         executable_path=(gecko+'.exe'),
#         options=options,
#     )
#     driver.set_window_size(1920, 1080)
#     # driver.maximize_window()

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

    def extract_from_document(self, document):
        """ Navigate to URL or local file (document), inject script, return
        extract, catch any exceptions """
        try:
            self.driver.get(document)
            time.sleep(10)
        except Exception as e:
            self.quit(m='FAILED EXTRACT: {}'.format(e))

        extract = self.driver.execute_script(self.script)
        return extract

    def process_url(self, url, store=True, screenshot=False):
        """ Extract from a url """
        return self.extract_from_document(url)

    def process_file(self, vd, page, screenshot=False):
        """ Extract from local file """

        local_file = 'file://{}'.format( os.path.join(vd, page) )

        extract = self.extract_from_document(local_file)

        if screenshot:
            f = page.split('.')[0]
            n = f + '.png'
            sd = os.path.join('data', '_screenshots', n)

            self.driver.save_screenshot(sd)

        return extract
