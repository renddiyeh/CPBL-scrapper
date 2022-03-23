from turtle import st
from bs4 import BeautifulSoup
import requests
import re
import csv
from datetime import datetime, timedelta
import sys


def getRainData(d):
    response = requests.get('https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=466940&stname=%25E5%259F%25BA%25E9%259A%2586&datepicker=' + d + '&altitude=26.7m#')
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('#MyTable > tbody > tr')
    hours = []
    for row in rows:
        if (row.select_one('td')):
            hour = row.select_one('td:nth-child(1)').get_text().strip()
            precp = row.select_one('td:nth-child(11)').get_text().strip()
            precpHr = row.select_one('td:nth-child(12)').get_text().strip()
            hours.append([hour, precp, precpHr])
    print(f"{d} done")
    return hours
    

# all_prices = []
# for d in range(200, 318):
#     data = getRainData(d)
#     all_prices.append(data)
all_data = []
date_start = datetime.strptime('2021-01-01', "%Y-%m-%d")
for d in range(365):
    date_str = datetime.strftime(date_start, "%Y-%m-%d")
    try:
        data = getRainData(date_str)
        for datum in data:
            all_data.append([date_str] + datum)
    except:
        e = sys.exc_info()[0]
        print(e)
        print(f"{date_str} failed")
    date_start = date_start + timedelta(days=1)


with open('rain_data.csv', 'w', encoding='utf-8', newline='') as f:
    write = csv.writer(f)
    write.writerow(['date', 'hour', 'precp', 'precpHr'])
    write.writerows(all_data)