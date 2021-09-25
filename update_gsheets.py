# Usage: after manually editing "Raw Data For Stats" tab to cover new drafts,
#        run this tool to fully automatically update "Card Stats" and "Seat Stats"

import pickle
import os.path
import csv
import compute_vrd_stats
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID of the stats spreadsheet (this one is a test copy)
spreadsheet_id = '12LKNtBof-FTxO6Zyzrv8MN-2AEexw5aHV_YnlwD46WM'
all_drafts_range = 'Raw Material For Stats!A103:CA'

cur_service = None
def get_service():
    global cur_service
    if cur_service is None:
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('input/token.pickle'):
            with open('input/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'input/gsheet_credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('input/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        cur_service = build('sheets', 'v4', credentials=creds)
    return cur_service

def scrape_drafts_tsv():
    service = get_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=all_drafts_range).execute()
    values = result.get('values', [])

    if not values:
        raise Exception('No draft data found in the google sheet')
         
    outf = open("output/scraped_drafts.tsv", "w", encoding="utf-8")        
    tsv_output = csv.writer(outf, delimiter='\t')
    tsv_output.writerows(values)
    print ("Wrote basic draft data to output/scraped_drafts.tsv")
    return len(values)

# the api demands we use a numeric id for the tabs. this helper function lets me retrieve the id given a known name
def get_sheet_id_by_name(service, name):
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    for _sheet in spreadsheet['sheets']:
        if _sheet['properties']['title'] == name:
            return _sheet['properties']['sheetId']    

# if it's a number, insert it into sheets as a number. otherwise as a string.
def describe_val(v):
    if v.replace('.','',1).isdigit():
        return {'numberValue': v}
    else:
        return {'stringValue': v}

# same method for both card stats and seat stats.
def upload_sheet_data(sheetName, startRowIdx, startColIdx, nestedArrays):
    service = get_service()
    maxHeight = len(nestedArrays) + 1 # extra for header row
    maxWidth = len(nestedArrays[0])

    sheetId = get_sheet_id_by_name(service, sheetName)

    update_rows = [{'values': [{'userEnteredValue': describe_val(f)} for f in e]} for e in nestedArrays]
    update_range = {'sheetId': sheetId, 'startRowIndex': startRowIdx, 'startColumnIndex': startColIdx, 'endColumnIndex': startColIdx + maxWidth}
    body = {
        'requests': [
            {
                'updateSheetProperties': { # first make sure the sheet is big enough
                    'properties': {
                        'sheetId': sheetId,
                        'gridProperties': {
                            'rowCount': maxHeight
                        }
                    },
                    "fields": "gridProperties(rowCount)"
                }
            },
            {
                "copyPaste": { # if we expanded it, we need to copy the formulas on the side to the new area
                    "source": {
                        "sheetId": sheetId,
                        "startRowIndex": 1, # grab the first line
                        "endRowIndex": 2
                    },
                    "destination": {
                        "sheetId": sheetId,
                        "startRowIndex": 2,
                        "endRowIndex": maxHeight + 1 # paste the formulas down to the bottom
                    },
                    "pasteType": "PASTE_FORMULA"
                }
            },
            {    # add the actual data
                'updateCells': {'rows': update_rows, 'range': update_range, 'fields': 'userEnteredValue'}
            },
            {
                "sortRange": {
                    "range": {
                        "sheetId": sheetId,
                        "startRowIndex": 1,
                    },
                    "sortSpecs": [
                        {
                            "dimensionIndex": 4,    # column 4 is coincidentally a good sort key for cards AND seats
                            "sortOrder": "ASCENDING"
                        }
                    ]
                }
            }
        ]
    }
    
    request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body)
    request.execute()

def upload_vintage_cards():
    sheetName = "allcards"
    service = get_service()
    cards = []
    with open("output/vintage_cards.txt", "r") as f:
        for line in f:
            cards.append([line.strip()])

    maxHeight = len(cards) + 1

    sheetId = get_sheet_id_by_name(service, sheetName)

    update_rows = [{'values': [{'userEnteredValue': describe_val(f)} for f in e]} for e in cards]
    update_range = {'sheetId': sheetId,
                    'startRowIndex': 1,
                    'startColumnIndex': 0}
    body = {
        'requests': [
            {
                'updateSheetProperties': { # first make sure the sheet is big enough
                    'properties': {
                        'sheetId': sheetId,
                        'gridProperties': {
                            'rowCount': maxHeight
                        }
                    },
                    "fields": "gridProperties(rowCount)"
                }
            },
            {    # add the actual data
                'updateCells': {'rows': update_rows, 'range': update_range, 'fields': 'userEnteredValue'}
            }
        ]
    }

    request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body)
    request.execute()


def read_tsv_to_arrs(filename):
    outarr = []
    with open(filename, 'r') as f:
        for line in f:
            arr = line.split("\t")            
            outarr.append([s.strip() for s in arr])
    return outarr
    
if __name__ == '__main__':   
    print("Getting basic draft data from google sheet...")
    rows = scrape_drafts_tsv()
    print("Found " + str(rows) + " rows (" + str(rows / 8) + " drafts)")
    compute_vrd_stats.compute_stats_of_file('output/scraped_drafts.tsv')
    doit = input("Inspect those stats files now. Upload them to the sheet? (y/N)")
    if doit.lower() == "y":
        print ("Uploading card data...")
        card_data = read_tsv_to_arrs("output/card stats.tsv")
        upload_sheet_data("Card Stats", 1, 1, card_data)

        print ("Uploading seat data...")
        seat_data = read_tsv_to_arrs("output/seat stats.tsv")
        upload_sheet_data("Seat Stats", 1, 0, seat_data)

        print("Done")
    else:
        print ("Okay, not uploading. Done.")
    