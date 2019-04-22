from plugins.plugin import Plugin
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
plugin_name = 'Google'


class Google(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'Google test suite'
        self.tests = {
            'Search': self.search
        }

    def setup(self):
        self.driver = Firefox()

    def teardown(self):
        self.driver.quit()

    def search(self, text):
        self.driver.get('https://google.com')
        self.driver.find_element_by_name('q').send_keys(text)
        self.driver.find_element_by_name('q').send_keys(Keys.ENTER)
