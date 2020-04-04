from oauth2client.service_account import ServiceAccountCredentials
import gspread

# list expects a 3-tuple with name, email, password
def writeToSheet(keyfile, url, list):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        keyfile, scope)
    gc = gspread.authorize(credentials)
    wks = gc.open_by_url(url).sheet1
    wks.append_row(list)
