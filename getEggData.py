from bs4 import BeautifulSoup
import requests
import re
import csv

def getEggData(d):
    response = requests.get('https://tw.chinyieggs.com/egg_detail/' + str(d) + '/')
    soup = BeautifulSoup(response.text, 'html.parser')
    date = soup.select('body > div.wrapper > div.inside > div > div.R > div > table > tbody > tr:nth-child(1) > th')[0].text
    priceTxt = soup.select('body > div.wrapper > div.inside > div > div.R > div > table > tbody > tr:nth-child(4) > td:nth-child(2)')[0].text
    x = re.search("\d+", priceTxt)
    price = x.group()
    print(date + ': ' + price)
    return [date, price]

all_prices = []
for d in range(200, 318):
    data = getEggData(d)
    all_prices.append(data)

with open('eggPrice.csv', 'w', encoding='utf-8', newline='') as f:
    write = csv.writer(f)
    write.writerow(['date', 'price'])
    write.writerows(all_prices)