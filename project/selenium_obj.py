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
        self.driver = Driver_Config.driver
        self.script = open(script).read()

    def quit(self, m=None):
        """ Quit the driver """
        print('{} ...quitting'.format(m))
        self.driver.quit()

    def close(self):
        print('...closing driver')
        self.driver.close()

    def process_url(self, url):
        """ Inject script, catch exceptions """
        try:
            try:
                self.driver.get(url)
            except Exception as e:
                self.quit(m='failed to get url: {}'.format(e))

            extract = self.driver.execute_script(self.script)
            return extract

        except Exception as e:
            self.quit(m='failed to process_page: {}'.format(e))

    def process_file(self, vd, page, screenshot=False):
        """ Open local file """
        file = os.path.join(vd, page)
        try:
            self.driver.get('file://{}'.format(file))
        except Exception as e:
            self.quit(m='failed to open file: {}'.format(e))

        extract = self.driver.execute_script(self.script)

        if screenshot:
            f = page.split('.')[0]
            n = f + '.jpg'
            sd = os.path.join('data', '_screenshots', n)

            self.driver.save_screenshot(sd)

        return extract


# if __name__ == '__main__':

#     script = os.path.join(os.path.dirname(__file__), 'inject.js')
#     slnm_driver = Driver(script)

#     try:
#         extract = slnm_driver.process_url(url)

#         if extract:
#             print(extract)

#             # pass to database writer

#     finally:
#         slnm_driver.quit('Done.')
