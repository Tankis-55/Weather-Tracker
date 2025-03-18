import requests
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import seaborn as sns
import os
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file("credentials.json")

# Uploading the API key
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError(" Error: API_KEY was not found. Check .env!")

cities = ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt", "Stuttgart", "Düsseldorf", "Dresden", "Leipzig", "Nuremberg"]

# URL API
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

weather_data = []

# request the weather for each city
for city in cities:
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather_data.append({
            "City": city,
            "Temperature": data["main"]["temp"],
            "Humidity": data["main"]["humidity"],
            "Weather": data["weather"][0]["description"]
        })
    else:
        print(f" Error{city}: {response.status_code}, answer API: {response.json()}")

# save in Excel и CSV
df = pd.DataFrame(weather_data)

df.to_excel("weather_data.xlsx", index=False, engine="openpyxl")
df.to_csv("weather_data.csv", index=False)

print(" Data added to weather_data.csv and weather_data.xlsx")

# data analyse
if not df.empty:
    #  Average temperature
    avg_temp = df["Temperature"].mean()
    print(f"\n Average temperature in all cities: {avg_temp:.2f}°C")

    # The city with the highest temperature
    hottest = df.loc[df["Temperature"].idxmax()]
    print(f" The warmest city: {hottest['City']} ({hottest['Temperature']}°C)")

    # The city with the lowest temperature
    coldest = df.loc[df["Temperature"].idxmin()]
    print(f" The coldest city {coldest['City']} ({coldest['Temperature']}°C)")

    # Average humidity
    avg_humidity = df["Humidity"].mean()
    print(f"\n Average humidity: {avg_humidity:.2f}%")

    # The city with the highest humidity
    most_humid = df.loc[df["Humidity"].idxmax()]
    print(f" The wettest city: {most_humid['City']} ({most_humid['Humidity']}%)")

    #The city with the lowest humidity
    least_humid = df.loc[df["Humidity"].idxmin()]
    print(f" Driest city: {least_humid['City']} ({least_humid['Humidity']}%)")
    
    #  Temperature graph
    plt.figure(figsize=(8, 5))
    sns.barplot(x="City", y="Temperature", data=df, palette="coolwarm", legend=False)
    plt.title("Temperature in different German cities")
    plt.xlabel("Cty")
    plt.ylabel("Temerature (°C)")
    plt.xticks(rotation=45)
    plt.show ()

    # Humidity graph
    plt.figure(figsize=(8, 5))
    sns.barplot(x="City", y="Humidity", data=df, palette="Blues", legend=False)
    plt.title("Humidity in different German cities")
    plt.xlabel("cyty")
    plt.ylabel("Humidity (%)")
    plt.xticks(rotation=45)
    plt.show ()

else:
    print(" There is no data, reports will not be built!")

# 🔹 Setting up the Google API
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # open Google Sheet
    SPREADSHEET_NAME = "weather_data"
    try:
        spreadsheet = client.open(SPREADSHEET_NAME).sheet1  
    except gspread.exceptions.SpreadsheetNotFound:
        print(f" Тable {SPREADSHEET_NAME} was not found. Check the name and access!")
        exit()

    # Clearing befor uploding
    spreadsheet.clear()
    spreadsheet.update([df.columns.values.tolist()] + df.values.tolist())

    print("Data uploaded to Google Sheets")

except Exception as e:
    print(f" Misstake during uploading to Google Sheets: {e}")