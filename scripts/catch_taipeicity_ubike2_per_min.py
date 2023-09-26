import requests
import pandas as pd
import time
from datetime import datetime
import os

# Set API URLs
url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json" #taipei city
data_path = "./"

# Function to get data
def fetch_data_from_url(url):
    while True:
        try:
            response = requests.get(url, timeout=10) #try to get response in 10s
            response.raise_for_status() #raise HTTPError if no response
            return response.json()
        except requests.RequestException as e: #show error code to log
            print(f"Error fetching data from {url}. Retrying... Error: {e}")
            time.sleep(5) #retry after 5s

# Function to transform data and save the table
def get_and_save_data():
    data = fetch_data_from_url(url)

    #convert collected data (JSON) to DataFrame
    df = pd.DataFrame(data)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S') #time format
    file_path = os.path.join(data_path, f"data_{timestamp}.txt") #set file name with a time stamp

    #save DataFrame to .txt
    df.to_csv(file_path, sep='\t', index=False)

    print(f"Data saved at: {file_path} \t nrow={len(df)}") #write a log info for each saving process

# Infinite loop to run every 60 seconds
while True:
    start_time = time.time()
    get_and_save_data()
    elapsed_time = time.time() - start_time
    sleep_time = max(0, 60 - elapsed_time)
    time.sleep(sleep_time)

