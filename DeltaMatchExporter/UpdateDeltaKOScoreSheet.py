import csv
import sys
import time

import requests
import os.path
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


if __name__ == "__main__":
    # Get season and match number
    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: python3 UpdateDeltaKOScoreSheet.py <season_num> <match_num>")
        exit(1)
    if int(args[0]) not in range(1, 1000) and int(args[1]) not in range(1, 6):
        print("Season must be a number, and match must be in range 1 to 6")
        exit(1)

    season_num = int(args[0])
    match_num = int(args[1])

    # Convert match number to an index in spreadsheet
    match_num_to_idx_dict = {1: 'E', 2: 'F', 3: 'G', 4: 'H', 5: 'I', 6: 'J'}
    match_idx = match_num_to_idx_dict[match_num]

    # Define static variables
    SPREADSHEET_ID = '1sePzgP_ThJY0uXTxZPoeXrR73mKh8rBzxwhtK1bDHkc'
    RANGE_IDXS = range(4, 1000)
    PLAYER_BANK_RANGE = f'Season {season_num}!A4:A1000'
    PLAYER_MATCH_NAME_RANGE = f'Season {season_num}!D4:D1000'
    PLAYER_MATCH_SCORE_RANGE = f'Season {season_num}!{match_idx}4:{match_idx}1000'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # Grab file Evo backend website
    # If this doesn't work as expected, then download the csv and make sure the latest match data is accurate
    # If it isn't, then delete the last rows of the csv until it aligns with the latest valid match
    url = "https://match-export.evotm.com/delta-ko/download.php?match=1"
    response = requests.get(url)
    open(f"season_{season_num}_match_{match_num}.csv", "wb").write(response.content)

    # Read the relevant information out of the CSV
    with open(f'season_{season_num}_match_{match_num}.csv') as matchstats:
        reader = csv.DictReader(matchstats, delimiter=';')
        rows = reversed(list(reader))
        player_order = []
        for row in rows:
            player_order.insert(0, [row['ubiname'], int(row['position'])])
            if row['position'] == '1':
                break

    # Read the list of existing players on the sheet
    creds = None
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
    player_bank = result.get('values')
    if player_bank is not None:
        player_bank = [player_bank[i][0] for i in range(len(player_bank))]
    else:
        player_bank = []

    # Add in all players who do not exist in the player bank
    match_players = [player_order[i][0] for i in range(len(player_order))]
    players_to_add = []
    for player in match_players:
        if player not in player_bank:
            players_to_add.append([player])
    body = {'values': players_to_add}
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f'Season 2!A{RANGE_IDXS[0] + len(player_bank)}:A{RANGE_IDXS[0] + len(player_bank) + len(players_to_add) - 1}',
        valueInputOption="USER_ENTERED",
        body=body).execute()
    print(f"{result.get('updatedCells')} cells updated.")

    # Wait for a second because this can take some time
    # print("Waiting 10 seconds to avoid race condition...")
    # time.sleep(10)

    # Get the player list again from the scoresheet column (this will be used to update positions)
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=PLAYER_MATCH_NAME_RANGE).execute()
    player_locations_in_sheet = result.get('values')
    if player_locations_in_sheet is not None:
        player_locations_in_sheet = [player_locations_in_sheet[i][0] for i in range(len(player_locations_in_sheet))]
    else:
        player_locations_in_sheet = []
    position_write_locations = [''] * len(player_locations_in_sheet)
    for player_data in player_order:
        player_location_in_sheet = player_locations_in_sheet.index(player_data[0])
        position_write_locations[player_location_in_sheet] = [str(player_data[1])]

    # Finally write to the match's scoresheet column with all positions
    body = {'values': position_write_locations}
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f'Season 2!E{RANGE_IDXS[0]}:E{RANGE_IDXS[0] + len(position_write_locations) - 1}',
        valueInputOption="USER_ENTERED",
        body=body).execute()
    print(f"{result.get('updatedCells')} cells updated.")
