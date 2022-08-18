from calendar import month
from turtle import st
from bs4 import BeautifulSoup
import requests
import re
import csv
from datetime import datetime, timedelta
import sys
from dateutil.relativedelta import relativedelta

stations = [
["新北市", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=466880&stname=%25E6%259D%25BF%25E6%25A9%258B&datepicker={{date}}&altitude=9.7m"],
["臺北市", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=466920&stname=%25E8%2587%25BA%25E5%258C%2597&datepicker={{date}}&altitude=5.3m"],
["基隆市", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=466940&stname=%25E5%259F%25BA%25E9%259A%2586&datepicker={{date}}&altitude=26.7m"],
["花蓮縣", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=466990&stname=%25E8%258A%25B1%25E8%2593%25AE&datepicker={{date}}&altitude=16.1m"],
["宜蘭縣", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=467080&stname=%25E5%25AE%259C%25E8%2598%25AD&datepicker={{date}}&altitude=7.2m"],
["澎湖縣", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=467350&stname=%25E6%25BE%258E%25E6%25B9%2596&datepicker={{date}}&altitude=10.7m"],
["臺南市", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=467410&stname=%25E8%2587%25BA%25E5%258D%2597&datepicker={{date}}&altitude=40.8m"],
["高雄市", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=C0V440&stname=%25E9%25B3%25B3%25E5%25B1%25B1&datepicker={{date}}&altitude=27m"],
["嘉義市", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=467480&stname=%25E5%2598%2589%25E7%25BE%25A9&datepicker={{date}}&altitude=26.9m"],
["臺中市", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=467490&stname=%25E8%2587%25BA%25E4%25B8%25AD&datepicker={{date}}&altitude=84.04m"],
["新竹縣", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=467571&stname=%25E6%2596%25B0%25E7%25AB%25B9&datepicker={{date}}&altitude=26.9m"],
["屏東縣", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=C0R170&stname=%25E5%25B1%258F%25E6%259D%25B1&datepicker={{date}}&altitude=26m"],
["臺東縣", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=467660&stname=%25E8%2587%25BA%25E6%259D%25B1&datepicker={{date}}&altitude=9.0m"],
["南投縣", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=C0I460&stname=%25E5%258D%2597%25E6%258A%2595&datepicker={{date}}&altitude=110m"],
["雲林縣", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=C0K400&stname=%25E6%2596%2597%25E5%2585%25AD&datepicker={{date}}&altitude=65m"],
["彰化縣", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=C0G650&stname=%25E5%2593%25A1%25E6%259E%2597&datepicker={{date}}&altitude=34m"],
["金門縣", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=467110&stname=%25E9%2587%2591%25E9%2596%2580&datepicker={{date}}&altitude=47.9m"],
["連江縣", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=467990&stname=%25E9%25A6%25AC%25E7%25A5%2596&datepicker={{date}}&altitude=97.842m"],
["桃園市", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=C0C700&stname=%25E4%25B8%25AD%25E5%25A3%25A2&datepicker={{date}}&altitude=151m"],
["新竹市", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=C0D660&stname=%25E6%2596%25B0%25E7%25AB%25B9%25E5%25B8%2582%25E6%259D%25B1%25E5%258D%2580&datepicker={{date}}&altitude=65m"],
["苗栗縣", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=C0E750&stname=%25E8%258B%2597%25E6%25A0%2597&datepicker={{date}}&altitude=62m"],
["嘉義縣", "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=C0M760&stname=%25E6%25B0%2591%25E9%259B%2584&datepicker={{date}}&altitude=40m"],
]

all_data = []

def getWeatherData(city, url, month):
    print("getWeatherData: " + city)
    print("url: " + url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('#MyTable > tbody > tr')
    for row in rows:
        if (row.select_one('td')):
            day = row.select_one('td:nth-child(1)').get_text().strip()
            temp = row.select_one('td:nth-child(8)').get_text().strip()
            max_temp = row.select_one('td:nth-child(9)').get_text().strip()
            min_temp = row.select_one('td:nth-child(11)').get_text().strip()
            precp = row.select_one('td:nth-child(22)').get_text().strip()
            all_data.append([city, month, day, temp, max_temp, min_temp, precp])

def getMonthlyData(d):
    for station in stations:
        getWeatherData(station[0], station[1].replace("{{date}}", d), d)

date_start = datetime.strptime('2019-01-01', "%Y-%m-%d")
for d in range(12 * 3):
    date_str = datetime.strftime(date_start, "%Y-%m")
    try:
        getMonthlyData(date_str)
    except:
        e = sys.exc_info()[0]
        print(e)
        print(f"{date_str} failed")
    date_start = date_start + relativedelta(months=+1)


with open('weather_data.csv', 'w', encoding='utf-8', newline='') as f:
    write = csv.writer(f)
    write.writerow(['city', 'month', 'day', 'temp', 'max_temp', 'min_temp', 'precp'])
    write.writerows(all_data)