import requests
from bs4 import BeautifulSoup
from django.conf import settings
import os
import datetime

def get_historical_data_url(stock_symbol):
    today = datetime.date.today()
    file_path = os.path.join(settings.MEDIA_ROOT, f'{stock_symbol}_{today}.csv')
    
    # Check if file already exists for today
    if os.path.exists(file_path):
        return file_path  # Return path if already downloaded today

    # Construct the URL dynamically with the given stock symbol
    url = f'https://www.mubasher.info/markets/EGX/stocks/{stock_symbol}'
    
    # Send HTTP GET request to the website
    response = requests.get(url)
    if response.status_code != 200:
        return 'Failed to retrieve data'

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Navigate through the HTML structure to find the data URL
    mi_content = soup.find('div', class_="mi-content")
    if not mi_content:
        return 'mi-content division not found.'

    mi_main_content = mi_content.find('main', class_="mi-main-content")
    if not mi_main_content:
        return 'mi-main-content division not found.'

    historical_data_container = mi_main_content.find('div', attrs={"historical-data-url": True})
    if historical_data_container:
        # Assuming the URL is directly downloadable
        data_url = historical_data_container['historical-data-url']
        download_and_save_csv(data_url, file_path)
        return file_path
    else:
        return 'Historical data URL not found.'

def download_and_save_csv(data_url, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    response = requests.get(data_url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
