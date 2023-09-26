import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time

def fetch_data_from_url(url,Date):
    while True:
        try:
            response = requests.get(url.format(date=Date),timeout=30)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error fetching data. Retrying... Error: {e}")
            time.sleep(30)

#CWA Station TAIPEI (466920) 121.5148 25.0376
#base_url = "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=466920&stname=%25E8%2587%25BA%25E5%258C%2597&datepicker={date}&altitude=5.3m"
#CWA Station Wenshan (C0AC80) 121.5757 25.0023
#base_url = "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0AC80&stname=%25E6%2596%2587%25E5%25B1%25B1&datepicker={date}&altitude=40m" 
#CWA Station Xinyi (C0AC70) 121.5645 25.0378
#base_url = "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0AC70&stname=%25E4%25BF%25A1%25E7%25BE%25A9&datepicker={date}&altitude=71m"

#CWA Station Shipai (C0AI40) 121.5131 25.1155
base_url = "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0AI40&stname=%25E7%259F%25B3%25E7%2589%258C&datepicker={date}&altitude=35m"

start_date = datetime(2021, 8, 1)
end_date = datetime(2023, 8, 31)

for n in range(int((end_date - start_date).days) + 1):
    current_date = (start_date + timedelta(n)).strftime('%Y-%m-%d')
    response = fetch_data_from_url(base_url,current_date)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extracting info
    station_soup = soup.find("td", text=lambda t: "測站" in t if t else False)
    observation_station = station_soup.text.split(":")[1]
    date_soup = soup.find("td", text=lambda t: "觀測時間" in t if t else False)
    observation_date = date_soup.text.split(":")[1]
    if observation_date == current_date:
        print("Date checked",observation_date,observation_station)
    # Extracting data
    rows = soup.select("tr")
    results = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 10:
            hour = cols[0].text.strip() #01 to 24
            temperature = cols[3].text.strip() #celsius
            rainfall = cols[10].text.strip() #mm
            PrecpHour = cols[11].text.strip() #rain time in an hour 0.1 to 1hr
            SunShineHr = cols[12].text.strip() #sun shine time in an hour 0.1 to 1hr
            GloblRad = cols[13].text.strip() #solar exposur (MJ/㎡)
            Cloud = cols[16].text.strip() #cloud amount rate 1 to 10
            results.append([observation_date,hour,temperature,rainfall,PrecpHour,SunShineHr,GloblRad,Cloud])
    df = pd.DataFrame(results)
    df.to_csv('shipai_history_weather.txt',sep='\t',index=False,mode='a',header=False)
    time.sleep(2)

time.sleep(1800)
#CWA Station Neihu (C0A9F0) 121.5754 25.0794
base_url = "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0A9F0&stname=%25E5%2585%25A7%25E6%25B9%2596&datepicker={date}&altitude=35m" 

start_date = datetime(2021, 8, 1)
end_date = datetime(2023, 8, 31)

for n in range(int((end_date - start_date).days) + 1):
    current_date = (start_date + timedelta(n)).strftime('%Y-%m-%d')
    response = fetch_data_from_url(base_url,current_date)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extracting info
    station_soup = soup.find("td", text=lambda t: "測站" in t if t else False)
    observation_station = station_soup.text.split(":")[1]
    date_soup = soup.find("td", text=lambda t: "觀測時間" in t if t else False)
    observation_date = date_soup.text.split(":")[1]
    if observation_date == current_date:
        print("Date checked",observation_date,observation_station)
    # Extracting data
    rows = soup.select("tr")
    results = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 10:
            hour = cols[0].text.strip() #01 to 24
            temperature = cols[3].text.strip() #celsius
            rainfall = cols[10].text.strip() #mm
            PrecpHour = cols[11].text.strip() #rain time in an hour 0.1 to 1hr
            SunShineHr = cols[12].text.strip() #sun shine time in an hour 0.1 to 1hr
            GloblRad = cols[13].text.strip() #solar exposur (MJ/㎡)
            Cloud = cols[16].text.strip() #cloud amount rate 1 to 10
            results.append([observation_date,hour,temperature,rainfall,PrecpHour,SunShineHr,GloblRad,Cloud])
    df = pd.DataFrame(results)
    df.to_csv('neihu_history_weather.txt',sep='\t',index=False,mode='a',header=False)
    time.sleep(2)

time.sleep(1800)
#CWA Station Songshan (C0AH70) 121.5504 25.0487
base_url = "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0AH70&stname=%25E6%259D%25BE%25E5%25B1%25B1&datepicker={date}&altitude=34m"

start_date = datetime(2021, 8, 1)
end_date = datetime(2023, 8, 31)

for n in range(int((end_date - start_date).days) + 1):
    current_date = (start_date + timedelta(n)).strftime('%Y-%m-%d')
    response = fetch_data_from_url(base_url,current_date)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extracting info
    station_soup = soup.find("td", text=lambda t: "測站" in t if t else False)
    observation_station = station_soup.text.split(":")[1]
    date_soup = soup.find("td", text=lambda t: "觀測時間" in t if t else False)
    observation_date = date_soup.text.split(":")[1]
    if observation_date == current_date:
        print("Date checked",observation_date,observation_station)
    # Extracting data
    rows = soup.select("tr")
    results = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 10:
            hour = cols[0].text.strip() #01 to 24
            temperature = cols[3].text.strip() #celsius
            rainfall = cols[10].text.strip() #mm
            PrecpHour = cols[11].text.strip() #rain time in an hour 0.1 to 1hr
            SunShineHr = cols[12].text.strip() #sun shine time in an hour 0.1 to 1hr
            GloblRad = cols[13].text.strip() #solar exposur (MJ/㎡)
            Cloud = cols[16].text.strip() #cloud amount rate 1 to 10
            results.append([observation_date,hour,temperature,rainfall,PrecpHour,SunShineHr,GloblRad,Cloud])
    df = pd.DataFrame(results)
    df.to_csv('songshan_history_weather.txt',sep='\t',index=False,mode='a',header=False)
    time.sleep(2)

time.sleep(1800)
#CWA Station Guandu (C1AC50) 121.4693 25.1334
base_url = "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C1AC50&stname=%25E9%2597%259C%25E6%25B8%25A1&datepicker={date}&altitude=111m" 

start_date = datetime(2021, 8, 1)
end_date = datetime(2023, 8, 31)

for n in range(int((end_date - start_date).days) + 1):
    current_date = (start_date + timedelta(n)).strftime('%Y-%m-%d')
    response = fetch_data_from_url(base_url,current_date)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extracting info
    station_soup = soup.find("td", text=lambda t: "測站" in t if t else False)
    observation_station = station_soup.text.split(":")[1]
    date_soup = soup.find("td", text=lambda t: "觀測時間" in t if t else False)
    observation_date = date_soup.text.split(":")[1]
    if observation_date == current_date:
        print("Date checked",observation_date,observation_station)
    # Extracting data
    rows = soup.select("tr")
    results = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 10:
            hour = cols[0].text.strip() #01 to 24
            temperature = cols[3].text.strip() #celsius
            rainfall = cols[10].text.strip() #mm
            PrecpHour = cols[11].text.strip() #rain time in an hour 0.1 to 1hr
            SunShineHr = cols[12].text.strip() #sun shine time in an hour 0.1 to 1hr
            GloblRad = cols[13].text.strip() #solar exposur (MJ/㎡)
            Cloud = cols[16].text.strip() #cloud amount rate 1 to 10
            results.append([observation_date,hour,temperature,rainfall,PrecpHour,SunShineHr,GloblRad,Cloud])
    df = pd.DataFrame(results)
    df.to_csv('guandu_history_weather.txt',sep='\t',index=False,mode='a',header=False)
    time.sleep(2)
