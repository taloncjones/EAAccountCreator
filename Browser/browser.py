import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

LOGGER = logging.getLogger(__name__)

MAX_RETRIES = 5


class Browser:
    def __init__(self, browserType, browserPath, email, username, password):
        self.browserType = browserType.lower()
        self.browserPath = browserPath
        self.browser = self.start()
        self.email = email
        self.username = username
        self.password = password

    def start(self):
        if self.browserType == 'chrome':
            ch_options = webdriver.ChromeOptions()
            ch_options.add_argument('--window-size=500,500')
            ch_options.add_argument('--window-position=-2000,0')
            return webdriver.Chrome(self.browserPath, options=ch_options)
        elif self.browserType == 'mozilla':
            mz_options = webdriver.FirefoxOptions()
            mz_options.add_argument('--width=600')
            mz_options.add_argument('--height=600')
            driver = webdriver.Firefox(self.browserPath, options=mz_options)
            driver.set_window_position(-2000, 0)
            return driver

    def quit(self):
        self.browser.quit()

    def goToURL(self, url):
        for i in range(0, MAX_RETRIES):
            iteration = i + 1
            while True:
                try:
                    self.browser.get(url)
                    WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located((By.ID, 'email')))
                except TimeoutException as err:
                    LOGGER.debug(err)
                    if (iteration == MAX_RETRIES):
                        raise ValueError(
                            "Maximum number of retries hit: {i}. Aborting execution".format(i=MAX_RETRIES))
                    break
                return

    typeSelector = {
        'id': By.ID,
        'class': By.CLASS_NAME,
        'xpath': By.XPATH,
    }

    def byLookup(self, lookupType):
        '''Returns By.ID from typeSelector based on lookupType. If lookupType not found in typeSelector, sys.exit() with error.'''
        selected = self.typeSelector.get(lookupType)
        if selected:
            return selected
        else:
            self.quit()
            sys.exit('Error: Invalid lookupType')

    def checkFor(self, id, lookupType='id'):
        '''
        Checks for element where lookupType = id
        id (str): What to look for on page
        [lookupType] (str): What <id> is. e.g. 'id', 'class'
        '''
        search = (self.byLookup(lookupType), id)
        try:
            return self.browser.find_element(*search).is_displayed()
        except NoSuchElementException:
            return False

    def showWindow(self):
        self.browser.set_window_position(0, 0)

    def hideWindow(self):
        self.browser.set_window_position(-2000, 0)

    def fillText(self, id, text):
        try:
            textID = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.ID, id))
            )
            textID.send_keys(text)
        except TimeoutException:
            self.showWindow()
            LOGGER.debug('Error: Could not find text field: {1}'.format(id))
            exit(1)

    def clickButton(self, id, lookupType='id'):
        search = (self.byLookup(lookupType), id)
        try:
            buttonID = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(search)
            )
            buttonID.click()
        except TimeoutException:
            self.showWindow()
            LOGGER.debug(
                'Error: Could not find button with {1}: {2}'.format(lookupType, id))
            exit(1)

    def keyDown(self, num=1):
        for _ in range(num):
            ActionChains(self.browser).send_keys(Keys.ARROW_DOWN).perform()

    def keySpace(self, num=1):
        for _ in range(num):
            ActionChains(self.browser).send_keys(Keys.SPACE).perform()

    def moveToNext(self, num=1):
        for _ in range(num):
            ActionChains(self.browser).send_keys(Keys.TAB).perform()
