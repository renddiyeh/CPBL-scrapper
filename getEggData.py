from turtle import st
from bs4 import BeautifulSoup
import requests
import re
import csv

def getEggData(d):
    response = requests.get('https://tw.chinyieggs.com/egg_detail/' + str(d) + '/')
    soup = BeautifulSoup(response.text, 'html.parser')
    date = soup.select('body > div.wrapper > div.inside > div > div.R > div > table > tbody > tr:nth-child(1) > th')[0].text
    
    prices = []
    for n in range(4, 7):
        priceEle = soup.select('body > div.wrapper > div.inside > div > div.R > div > table > tbody > tr:nth-child(' + str(n) + ') > td:nth-child(2)')[0]
        priceTxt = priceEle.get_text(strip=True, separator='\n').splitlines()
        if n > 4:
            prices.append(priceTxt[1])
        else:
            x = re.search("\d+", priceTxt[0])
            prices.append(x.group())
    return [date] + prices

all_prices = []
for d in range(200, 318):
    data = getEggData(d)
    all_prices.append(data)

with open('eggPrice.csv', 'w', encoding='utf-8', newline='') as f:
    write = csv.writer(f)
    write.writerow(['date', '雞蛋', '洗選蛋', 'CAS'])
    write.writerows(all_prices)