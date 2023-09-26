import requests
import pandas as pd
import time
from datetime import datetime
import os

# Set API URLs
url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
data_path = "./"

def fetch_data_from_url(url):
    while True:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data from {url}. Retrying... Error: {e}")
            time.sleep(5)

def get_and_save_data():
    # Fetch data from both URLs with retry mechanism
    data = fetch_data_from_url(url)
    
    # Combine data from both URLs
    all_data = data

    # Convert collected data to DataFrame
    df = pd.DataFrame(all_data)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    file_path = os.path.join(data_path, f"data_{timestamp}.txt")

    # Save DataFrame to .txt
    df.to_csv(file_path, sep='\t', index=False)

    print(f"Data saved at: {file_path} \t nrow={len(df)}")

# Infinite loop to run every 60 seconds
while True:
    start_time = time.time()
    get_and_save_data()
    elapsed_time = time.time() - start_time
    sleep_time = max(0, 60 - elapsed_time)
    time.sleep(sleep_time)

