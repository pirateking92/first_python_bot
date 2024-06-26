import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the Google Sheets API scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID of the Google Sheet to update
SPREADSHEET_ID = "1TBpLTpAsucY_aYz5qF4DN6bI90DQQ64v3AUzPA6zqeI"
RANGE_NAME = "Sheet1!A1"  # The range to update

# scraping logic from here to line 42
url = "https://myanimelist.net/topanime.php?type=movie"

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')

# Find all anime listings based on the common css selector
listings = soup.find_all('tr', class_='ranking-list')


def req_scrape():
    data = []
    for listing in listings:
        title = listing.find(
            'h3', class_='fl-l fs14 fw-b anime_ranking_h3').text.strip()
        score = listing.find(
            'div', class_='js-top-ranking-score-col di-ib al').text.strip()
        data.append({"Title": title, "Score": score})

    df = pd.DataFrame(data)
    df.to_csv('anime_ranking.csv', index=False)

    return df


def upload_to_google_sheets():
    """Uploads data from the CSV to Google Sheets."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Load data from CSV
        df = pd.read_csv("anime_ranking.csv")

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
# req_scrape()

# Upload the CSV data to Google Sheets
# upload_to_google_sheets()
