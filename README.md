Overview

Weather Tracker is a Python-based project that retrieves real-time weather data from OpenWeatherMap, processes and visualizes the data, and stores it locally or in Google Sheets. It is automated to update every three hours using cron.

Features

Fetches real-time weather data for multiple cities.

Stores data in CSV and Excel formats.

Visualizes temperature and humidity trends using Matplotlib and Seaborn.

Supports automated updates with cron jobs.

Uploads weather data to Google Sheets via Google API.

Installation

Clone the repository:

git clone https://github.com/yourusername/weather_tracker.git
cd weather_tracker

API_KEY=your_openweathermap_api_key

Automation (scheduled launch via cron):
open the editor crontab -e

running every 3 hours (in 00:00, 03:00, 06:00 and so on.)
paste 0 */3 * * * /path to python in venv  /path to the script /weather_analysis/weather_scraper.py

Usage

Run the script manually:

python weather_scraper.py


Google Sheets Integration

Enable Google Sheets API in Google Cloud Console.

Download credentials.json and place it in the project folder.

Run upload_to_sheets.py to upload weather data.
