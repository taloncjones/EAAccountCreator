import logging
import imaplib
import email
import json
from email.parser import HeaderParser

LOGGER = logging.getLogger(__name__)


# Takes in a dictionary of arguments and searches for emails matching those parameters
def search_for(con, email_info):
    search = ''
    for k, v in email_info.items():
        if type(v) is bool:
            if v:
                search += '{} '.format(k.upper())
        else:
            search += '{0} "{1}" '.format(k.upper(), v)

    result, data = con.search(None, search[:-1])
    return data


# Takes in list of email IDs and returns list of emails
def get_emails(con, result_bytes):
    msgs = []
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs


# Connects to email via IMAP using user, password
def connect(user, password):
    LOGGER.debug('Connecting to inbox...')
    con = imaplib.IMAP4_SSL('imap.gmail.com', '993')
    con.login(user, password)
    con.select('Inbox')
    LOGGER.debug('Connected.')
    return con


# Loads user, password from credentialsFile
def get_credentials(credentialsFile):
    if type(credentialsFile) is tuple:
        return (credentialsFile[0], credentialsFile[1])

    with open(credentialsFile, 'r') as f:
        data = json.load(f)

    return (data['email'], data['app_password'])

# Get email from credentialsFile
def get_email_address(credentialsFile):
    email, password = get_credentials(credentialsFile)
    return email

# Get password from credentialsFile
def get_email_password(credentialsFile):
    email, password = get_credentials(credentialsFile)
    return password


# Takes in credentials, email_info and returns EA verification code
def get_verification_code(credentialsFile, email_info):
    LOGGER.debug('Getting verification code...')
    parser = HeaderParser()
    con = connect(*get_credentials(credentialsFile))
    msgs = get_emails(con, search_for(con, email_info))

    for msg in msgs[::-1]:
        for sent in msg:
            if type(sent) is tuple:
                content = str(sent[1], 'utf-8')
                data = str(content)
                headers = parser.parsestr(data)
                subject = headers['Subject']
                code = subject.split(' ')[-1]
                LOGGER.debug('Verification Code: {}'.format(code))
                return code
