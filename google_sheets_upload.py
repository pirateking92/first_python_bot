import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

from requests_scraper import req_scrape

# Define the Google Sheets API scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID of the Google Sheet to update
SPREADSHEET_ID = "1TBpLTpAsucY_aYz5qF4DN6bI90DQQ64v3AUzPA6zqeI"
RANGE_NAME = "Sheet1!A1"  # The range to update


def upload_to_google_sheets():
    """Uploads data from the CSV to Google Sheets."""
    creds = None
    if os.path.exists(
            "/Users/mattdoyle/Desktop/Coding/Python/twitter_bot/token.json"):
        creds = Credentials.from_authorized_user_file(
            "/Users/mattdoyle/Desktop/Coding/Python/twitter_bot/token.json",
            SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "/Users/mattdoyle/Desktop/Coding/Python/twitter_bot/credentials.json",
                SCOPES)
            creds = flow.run_local_server(port=0)

        with open(
                "/Users/mattdoyle/Desktop/Coding/Python/twitter_bot/token.json",
                "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Load data from CSV
        df = pd.read_csv(
            "/Users/mattdoyle/Desktop/Coding/Python/twitter_bot/top_airing_anime.csv"
        )

        # Convert DataFrame to list of lists
        values = [df.columns.tolist()] + df.values.tolist()

        # Prepare the data for the API
        body = {"values": values}

        # Write data to Google Sheets
        result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                       range=RANGE_NAME,
                                       valueInputOption="RAW",
                                       body=body).execute()

        print(f"{result.get('updatedCells')} cells updated.")

    except HttpError as err:
        print(err)


# Scrape data and save to CSV
req_scrape()

# Upload the CSV data to Google Sheets
upload_to_google_sheets()
