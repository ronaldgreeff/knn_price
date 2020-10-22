import os
import csv
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class Driver_Config():
    """ Consistant driver config """

    options = webdriver.ChromeOptions()

    options.add_argument('--ignore-certificate-errors')
    options.add_argument("user-data-dir=C:\\Path") #Path to your chrome profile

    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    driver.set_window_size(1920, 1080)


class Driver(Driver_Config):
    """ Main driver for navigating to webpage and interacting with it """

    def __init__(self, script):
        """ Initiate driver and load script """
        self.driver = Driver_Config.driver
        self.script = open(script).read()


    def quit(self, m=None):
        """ Quit the driver. Print a message if provided """
        if m:
            print( '{}'.format(m) )
        self.driver.quit()


    def get_page(self, page, sleep=10):
        """ Navigate to URL or local file (page), inject script, return
        extract, catch any exceptions """
        try:
            self.driver.get(page)
            time.sleep(sleep)
        except Exception as e:
            self.quit(m='get_page failed'.format(e))

        extract = self.driver.execute_script(self.script)
        return extract


    def save_screenshot(self, location):
        """ Save a screenshot - requires the full path name """
        self.driver.save_screenshot(location)


    def process_file(self, dir, filename, screenshot=None):
        """ Extract from local file """
        local_file = 'file://{}'.format( os.path.join(dir, filename) )
        return self.get_page(local_file)



# Details of Firefox error:
# "firefox not loading beautybay."
# todo: look into it
# todo: Store both FF and Chrome driver configs in /configs

# class Driver_Config():
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
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
