from bs4 import BeautifulSoup
import json
import requests
import os

years = {
    "2021": 300,
    "2020": 240,
    "2019": 240,
    "2018": 240,
    "2017": 240,
    "2016": 240,
    "2015": 240,
    "2014": 240,
    "2013": 240,
    "2012": 240,
    "2011": 240,
    "2010": 240,
    "2009": 240,
    "2008": 300,
    "2007": 300,
    "2006": 300,
    "2005": 300,
    "2004": 300,
    "2003": 300,
    "2002": 180,
    "2001": 180,
    "2000": 180,
    "1999": 278,
    "1998": 315,
    "1997": 336,
    "1996": 300,
    "1995": 300,
    "1994": 270,
    "1993": 270,
    "1992": 180,
    "1991": 180,
    "1990": 180,
}

def parse_json(d):
    for k in d:
        if isinstance(d[k], str):
            d[k] = json.loads(d[k])
    return d


def getGameData(year, gameNo):
    session = requests.Session()
    response = session.get('https://www.cpbl.com.tw/box/index', verify = False)
    soup = BeautifulSoup(response.text, 'html.parser')
    token = soup.find(attrs={"name": "__RequestVerificationToken"})

    params = {
        "__RequestVerificationToken": token,
        "GameSno": gameNo,
        "KindCode": "A",
        "Year": year,
    }

    try:
        response = session.post('https://www.cpbl.com.tw/box/getlive', params = params, verify = False)

        jsonData = response.json()
        dir = 'data/' + str(year)
        if not os.path.exists(dir):
            os.makedirs(dir)

        with open(dir + '/' + str(gameNo) + '.json', 'w', encoding='utf-8') as f:
            json.dump(parse_json(jsonData), f, ensure_ascii=False)
    except:
        print('error for ' + str(year) + ' game ' + str(gameNo))

def getYearData(year):
    games = years[str(year)]
    for game in range(games):
        getGameData(year, game + 1)

for year in range(2009, 2022):
    getYearData(year)