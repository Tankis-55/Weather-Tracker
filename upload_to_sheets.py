import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Google Sheets
SPREADSHEET_ID = "1..."  #ID from my sheet
SHEET_NAME = "Sheet1" 

# Connecting to Google Sheets via the API
creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# Uploading data from a CSV file
df = pd.read_csv("weather_data.csv")

# Sending data to Google Sheets
sheet.clear()  # Clearing the table before uploading
sheet.update([df.columns.values.tolist()] + df.values.tolist())

print(" The data has been successfully uploaded to Google Sheets!")
