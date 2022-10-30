import csv
import requests
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SPREADSHEET_ID = '1sePzgP_ThJY0uXTxZPoeXrR73mKh8rBzxwhtK1bDHkc'
PLAYER_BANK_RANGE = 'Season 2!A3:A1000'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

if __name__ == "__main__":
    # # Grab file Evo backend website
    # url = "https://match-export.evotm.com/delta-ko/download.php?match=1"
    # response = requests.get(url)
    # open("match.csv", "wb").write(response.content)
    #
    # # Read the relevant information out of the CSV
    # with open('match.csv') as matchstats:
    #     reader = csv.DictReader(matchstats, delimiter=';')
    #     rows = reversed(list(reader))
    #     player_order = []
    #     for row in rows:
    #         player_order.insert(0, [row['ubiname'], int(row['position'])])
    #         if row['position'] == '1':
    #             break
    #     print(player_order)

    # Read the list of existing players on the sheet
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=PLAYER_BANK_RANGE).execute()
    values = result.get('values')
    print(values)