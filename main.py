import sys
import os
import time
import random
import string
import contextlib
import urllib.request
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

EA_URL = 'https://signin.ea.com/p/web2/create?initref=https%3A%2F%2Faccounts.ea.com%3A443%2Fconnect%2Fauth%3Fresponse_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fwww.ea.com%252Flogin_check%26state%3De0cf8241-b0cf-446d-abdf-1c81ce5ea3ac%26client_id%3DEADOTCOM-WEB-SERVER%26display%3Dweb%252Fcreate'
USER_CHECK_URL = 'https://signin.ea.com/p/ajax/user/checkOriginId?originId='


class Browser:
  def __init__(self, browserVer, email, username, password):
    self.browserVer = browserVer
    self.browser = self.start()
    self.email = email
    self.username = username
    self.password = password

  def resource_path(self, relative_path):
    '''
    Returns the absolute location of file at relative_path.
    relative_path (str): The relative location of the file in question
    '''
    # sys._MEIPASS raises an error, but is used by pyinstaller to merge chromedriver into a single executable
    try:
      base_path = sys._MEIPASS
    except Exception:
      base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

  def start(self):
    if self.browserVer == 'Chrome':
      ch_options = webdriver.ChromeOptions()
      ch_options.add_argument('--window-size=500,500')
      ch_options.add_argument('--window-position=-2000,0')
      return webdriver.Chrome(self.resource_path('chromedriver'), options=ch_options)
    elif self.browserVer == 'Mozilla':
      mz_options = webdriver.FirefoxOptions()
      mz_options.add_argument('--width=600')
      mz_options.add_argument('--height=600')
      driver = webdriver.Firefox(executable_path=self.resource_path('geckodriver'), options=mz_options)
      driver.set_window_position(-2000,0)
      return driver

  def printAll(self):
    print(f'Email: {self.email}')
    print(f'User: {self.username}')
    print(f'Pass: {self.password}')

  def quit(self):
    self.browser.quit()

  def goToURL(self, url):
    self.browser.get(url)

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
    except TimeoutException:
      self.showWindow()
      sys.exit(f'Error: Could not find text field: {id}')

    textID.send_keys(text)

  def clickButton(self, id, lookupType='id'):
    search = (self.byLookup(lookupType), id)
    try:
      buttonID = WebDriverWait(self.browser, 10).until(
          EC.element_to_be_clickable(search)
      )
    except TimeoutException:
      self.showWindow()
      sys.exit(f'Error: Could not find button with {lookupType}: {id}')

    buttonID.click()

  def keyDown(self, num=1):
    for _ in range(num):
      ActionChains(self.browser).send_keys(Keys.ARROW_DOWN).perform()

  def keySpace(self, num=1):
    for _ in range(num):
      ActionChains(self.browser).send_keys(Keys.SPACE).perform()

  def moveToNext(self, num=1):
    for _ in range(num):
      ActionChains(self.browser).send_keys(Keys.TAB).perform()


def createAccount(browserVer, baseEmail, username):
  email = randomEmail(baseEmail, 12)
  password = randomPassword(16)
  browser = Browser(browserVer, email, username, password)
  browser.goToURL(EA_URL)

  # Initial Email Check
  browser.fillText('email', email)
  browser.clickButton('btn-next')

  # Username, Password, Security Q
  browser.fillText('originId', browser.username)
  browser.fillText('password', browser.password)
  browser.fillText('confirmPassword', browser.password)
  browser.moveToNext()
  browser.keyDown()
  browser.fillText('securityAnswer', browser.username)

  # DoB
  # EA uses DIVs and classes to control and display their dropdowns... Navigating with TAB and ARROWS is a bit easier
  browser.moveToNext(2)
  browser.keyDown()
  browser.moveToNext()
  browser.keyDown()
  browser.moveToNext()
  browser.keyDown(20)

  # Captcha, Checkboxes
  humanCheck = browser.checkFor('captcha-container2')
  if browser.browserVer == 'Chrome':
    browser.clickButton('contact-me-container')
    browser.clickButton('read-accept-container')
  elif browser.browserVer == 'Mozilla':
    browser.moveToNext(4 if humanCheck else 1)
    browser.keySpace()
    browser.moveToNext()
    browser.keySpace()

  # If Captcha, wait for human to solve, then continue
  if humanCheck:
    verifyHuman = False
    browser.showWindow()
    print('Captcha detected! Please complete captcha to continue...')
    while not verifyHuman:
      verifyHuman = browser.checkFor('fc_meta_success_text', 'class')
    browser.hideWindow()

  browser.clickButton('submit-btn')

  # Skip real name info
  browser.clickButton('btn-skip', 'class')

  print('\n\nCreated:')
  browser.printAll()

  with open('accounts.txt', 'a') as file:
    with contextlib.redirect_stdout(file):
      file.write(f'Account:\n')
      browser.printAll()
      file.write('\n')

  # Wait for verification code
  verify = input('Enter Verification: ')
  browser.fillText('emailVerifyCode', verify)
  browser.clickButton('btnMEVVerify')

  # Complete process and exit
  browser.clickButton('btnMEVComplete')
  browser.quit()

  print('Account creation complete.\n\n')


def randomPassword(size):
  letters = string.ascii_letters
  numbers = string.digits
  lsize = int(size * 3/4)
  randomLetters = ''.join(random.choice(letters) for i in range(lsize))
  randomNums = ''.join(random.choice(numbers) for i in range(size - lsize))
  return randomLetters + randomNums


def randomEmail(baseEmail, size):
  letters = string.ascii_letters
  randomString = ''.join(random.choice(letters) for i in range(size))
  atIndex = baseEmail.index('@')
  return baseEmail[:atIndex] + '+' + randomString + baseEmail[atIndex:]


if __name__ == '__main__':
  dir_path = os.path.dirname(os.path.realpath(__file__))
  print('Thanks for using the EA Account Creator tool! A list of created accounts (emails, usernames, passwords) can be found in your default home directory:')
  print(dir_path + '\n')
  try:
    while True:
      browserChoice = input(
          'Please select your browser:'
          '\n1)\tChrome'
          '\n2)\tMozilla'
          '\n'
      )
      if browserChoice == '1' or browserChoice.lower() == 'chrome':
        browserVer = 'Chrome'
        break
      elif browserChoice == '2' or browserChoice.lower() == 'mozilla':
        browserVer = 'Mozilla'
        break
      else:
        print('Invalid entry. Please choose the cooresponding number or text.')

    baseEmail = input('Base email address? (e.g. user@email.com) ')
    while True:
      choice = input('Create new account? ')
      if choice.lower() in {'y', 'yes'}:
        valid = False
        while not valid:
          username = input('Desired username: ')
          with urllib.request.urlopen(USER_CHECK_URL + username) as url:
            data = json.loads(url.read().decode())
            valid = data['status']
          if not valid:
            print('Username not available.')
        createAccount(browserVer, baseEmail, username)
      elif choice.lower() in {'n', 'no'}:
        sys.exit(0)

  except KeyboardInterrupt:
    print('Exiting...')
    sys.exit(0)
