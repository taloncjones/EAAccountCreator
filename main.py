import sys
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

EA_URL = 'https://signin.ea.com/p/web2/create?initref=https%3A%2F%2Faccounts.ea.com%3A443%2Fconnect%2Fauth%3Fresponse_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fwww.ea.com%252Flogin_check%26state%3De0cf8241-b0cf-446d-abdf-1c81ce5ea3ac%26client_id%3DEADOTCOM-WEB-SERVER%26display%3Dweb%252Fcreate'


class Browser:
  def __init__(self, email, username, password):
    self.browser = self.start()
    self.email = email
    self.username = username
    self.password = password

  def start(self):
    ch_options = webdriver.ChromeOptions()
    ch_options.add_argument('--window-size=100,100')
    ch_options.add_argument('--window-position=0,0')
    return webdriver.Chrome('./chromedriver', options=ch_options)

  def printAll(self):
    print(f'Email: {self.email}')
    print(f'User: {self.username}')
    print(f'Pass: {self.password}')

  def quit(self):
    self.browser.quit()

  def goToURL(self, url):
    self.browser.get(url)

  def checkFor(self, id, id_or_class='id'):
    if id_or_class == 'id':
      search = (By.ID, id)
    elif id_or_class == 'class':
      search = (By.CLASS_NAME, id)
    else:
      sys.exit('Error: clickButton id_or_class value invalid')

    try:
      return len(self.browser.find_elements(*search)) > 0
    except NoSuchElementException:
      return False

  def fillText(self, id, text):
    textID = WebDriverWait(self.browser, 10).until(
        EC.element_to_be_clickable((By.ID, id))
    )
    textID.send_keys(text)

  def clickButton(self, id, id_or_class='id'):
    if id_or_class == 'id':
      search = (By.ID, id)
    elif id_or_class == 'class':
      search = (By.CLASS_NAME, id)
    else:
      sys.exit('Error: clickButton id_or_class value invalid')

    buttonID = WebDriverWait(self.browser, 10).until(
        EC.element_to_be_clickable(search)
    )
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


def createAccount(baseEmail, username):
  email = randomEmail(baseEmail, 12)
  password = randomPassword(16)
  browser = Browser(email, username, password)
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

  # Capcha, Checkboxes
  humanCheck = browser.checkFor('captcha-container2')
  browser.clickButton('contact-me-container')
  browser.clickButton('read-accept-container')

  # If Capcha, wait for human
  if humanCheck:
    input('Need human verification. Please complete and hit enter.')
  browser.clickButton('submit-btn')

  # Skip real name info
  browser.clickButton('btn-skip', 'class')

  print('\n\nCreated:')
  browser.printAll()

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
  try:
    baseEmail = input("Base email address? ")
    while True:
      choice = input("Create new account? ")
      if choice.lower() in {'y','yes'}:
        username = input("Desired username: ")
        createAccount(baseEmail, username)
      elif choice.lower() in {'n','no'}:
        sys.exit()

  except KeyboardInterrupt:
    print("Exiting...")
    sys.exit()
