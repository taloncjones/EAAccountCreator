import random
import string
import urllib.request
import json
import logging
import argparse
import time
import getpass
import sys
import os
import Browser.browser as Browser
import Sheet.sheet as Sheet
import Gmail.gmail as Gmail
import random

RUN_CONFIG = {}
RUN_CONFIG['EA_URL'] = 'https://signin.ea.com/p/web2/create?execution=e381040894s1&initref=https%3A%2F%2Faccounts.ea.com%3A443%2Fconnect%2Fauth%3Fdisplay%3Dweb%252Fcreate%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fwww.ea.com%252Flogin_check%26state%3D6e5e74f9-3dfa-4994-9a03-c925e0575061%26client_id%3DEADOTCOM-WEB-SERVER'

RUN_CONFIG['USER_CHECK_URL'] = 'https://signin.ea.com/p/ajax/user/checkOriginId?originId='
RUN_CONFIG['WORD_LIST'] = '/usr/share/dict/words'

LOGGER = logging.getLogger(__name__)

MAX_RETRIES = 5


def createAccount(browserType, browserPath, baseEmail, email_credentials, username):
	email = randomEmail(baseEmail, 10)
	password = randomPassword(16)
	browser = Browser.Browser(browserType, browserPath, email, username, password)
	browser.goToURL(RUN_CONFIG['EA_URL'])

	list = [browser.username, browser.email, browser.password]
	Sheet.writeToSheet(RUN_CONFIG['KEY_FILE'], RUN_CONFIG['GSHEET_URL'], list)

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
	browser.keyDown(25)

	# Captcha, Checkboxes
	humanCheck = browser.checkFor('captcha-container2')
	if browser.browserType == 'chrome':
		browser.clickButton('contact-me-container')
		browser.clickButton('read-accept-container')
	elif browser.browserType == 'mozilla':
		browser.moveToNext(4 if humanCheck else 1)
		browser.keySpace()
		browser.moveToNext()
		browser.keySpace()

	# If Captcha, wait for human to solve, then continue
	if humanCheck:
		verifyHuman = False
		browser.showWindow()
		LOGGER.debug('Captcha detected! Please complete captcha to continue...')
		while not verifyHuman:
			ret = input("Continue? Enter any character when ready") 
			verifyHuman = True if len(ret) > 0 else False

	browser.clickButton('submit-btn')

	# Skip real name info
	browser.clickButton('btn-skip', 'class')

	# Check email for verification code
	email_info = {}
	email_info['from'] = 'EA@e.ea.com'
	email_info['to'] = email
	email_info['subject'] = 'Your EA Security Code is'
	email_info['unseen'] = True
	for i in range(0, MAX_RETRIES):
		iteration = i + 1
		verify = Gmail.get_verification_code(email_credentials, email_info)
		if not verify:
			if (iteration == MAX_RETRIES):
				raise TimeoutError('Maximum number of verification code checks hit: {i}. Aborting...'.format(i=MAX_RETRIES))
			else:
				time.sleep(30)
		else:
			break
	browser.fillText('emailVerifyCode', verify)
	browser.clickButton('btnMEVVerify')

	# Complete process and exit
	browser.clickButton('btnMEVComplete')
	browser.quit()

	LOGGER.debug('Account creation complete.\n\n')

	return list



def randomPassword(size):
    letters = string.ascii_letters
    numbers = string.digits
    lsize = int(size * 3 / 4)
    randomLetters = ''.join(random.choice(letters) for i in range(lsize))
    randomNums = ''.join(random.choice(numbers) for i in range(size - lsize))
    return randomLetters + randomNums


def randomEmail(baseEmail, size):
    letters = string.ascii_letters
    randomString = ''.join(random.choice(letters) for i in range(size))
    atIndex = baseEmail.index('@')
    return baseEmail[:atIndex] + '+' + randomString + baseEmail[atIndex:]


def randomName():
	return random.choice(open(RUN_CONFIG['WORD_LIST']).read().splitlines()) + "TTV"



def nameAvailable(username):
    with urllib.request.urlopen(RUN_CONFIG['USER_CHECK_URL'] + username) as url:
        data = json.loads(url.read().decode())
        valid = data['status']
    return valid


def resource_path(relative_path):
    '''
    Returns the absolute location of file at relative_path.
    relative_path (str): The relative location of the file in question
    '''
    # sys._MEIPASS raises an error, but is used by pyinstaller to merge chromedriver into a single executable
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def main():
	if len(sys.argv) > 1:
		parser = argparse.ArgumentParser()
		parser.add_argument('driverType', help="Provide the type of selenium driver for this run e.g. chrome")
		parser.add_argument('driverPath', help="Provide the path of the selenium driver you'll use")
		parser.add_argument('keyFile', help="Provide the generic account's key file that has Edit access to the following GSheet")
		parser.add_argument('gsheetURL', help="Provide the Google Sheet URL where account details will be appended")
		parser.add_argument('emailCredentials', help="Provide the email app's credentials to access and read email")
		parser.add_argument('--noop', dest='noop', action='store_true',
							help="Provide flag --noop if you want the operation to be a no-op")
		parser.set_defaults(noop=False)

		# parse args
		args = parser.parse_args()
		RUN_CONFIG['DRIVER_TYPE'] = args.driverType
		RUN_CONFIG['DRIVER_PATH'] = args.driverPath
		RUN_CONFIG['KEY_FILE'] = args.keyFile
		RUN_CONFIG['GSHEET_URL'] = args.gsheetURL
		RUN_CONFIG['EMAIL_CREDENTIALS'] = args.emailCredentials
		RUN_CONFIG['NOOP'] = args.noop

		logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

		if args.noop:
			LOGGER.debug('NO-OP run specified, dumping configuration parameters...')
			for k, v in RUN_CONFIG.items():
				print(k, v)
			exit(0)

		# extract base email
		RUN_CONFIG['BASE_EMAIL'] = Gmail.get_email_address(RUN_CONFIG['EMAIL_CREDENTIALS'])

		username = randomName()
		while not nameAvailable(username):
			username = randomName()
		try:
			list = createAccount(RUN_CONFIG['DRIVER_TYPE'], RUN_CONFIG['DRIVER_PATH'], RUN_CONFIG['BASE_EMAIL'], RUN_CONFIG['EMAIL_CREDENTIALS'], username)
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			LOGGER.debug(message)
		finally:
			LOGGER.debug('Cleaning up...')
	else:
		dir_path = os.path.dirname(os.path.realpath(__file__))
		print('A list of created accounts (emails, usernames, passwords) can be found in your default home directory:')
		print(dir_path + '\n')

		baseEmail = input("Enter base email (e.g. bob@gmail.com): ")
		emailCredentials = (baseEmail, getpass.getpass(prompt="Email password: "))

		driverNum = 0
		while driverNum not in {1,2}:
			driverNum = int(input("Choose your browser version (1 or 2):\n1. Chrome\n2. Firefox\n"))
		if driverNum == 1:
			driverType = 'chrome'
			driverPath = resource_path('chromedriver')
		else:
			driverType = 'mozilla'
			driverPath = resource_path('geckodriver')

		while True:
			choice = input("Make new account? (y/n): ")
			if choice.lower() in {'y','yes'}:
				username = randomName()
				while not nameAvailable(username):
					username = randomName()
				try:
					list = createAccount(driverType, driverPath, baseEmail, emailCredentials, username)
					print('Username: {}\nEmail: {}\nPassword: {}\n'.format(*list))
					with open('accounts.txt', 'a') as file:
						file.write('Account:\n')
						file.write('Username: {}\nEmail: {}\nPassword: {}\n'.format(*list))
						file.write('\n')
				except Exception as ex:
					template = "An exception of type {0} occurred. Arguments:\n{1!r}"
					message = template.format(type(ex).__name__, ex.args)
					LOGGER.debug(message)
				finally:
					LOGGER.debug('Cleaning up...')
			elif choice.lower() in {'n','no'}:
				break


if __name__ == "__main__":
    main()
