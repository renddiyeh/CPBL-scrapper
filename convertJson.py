import os
import json
import csv
from pathlib import Path

def getTeamStat(scoreBoard, abbr, key):
    cnt = 0
    for score in scoreBoard:
        if score['TeamAbbr'] == abbr:
            cnt += score[key]
    return cnt

def sortGameFile(fielName):
    name = Path(fielName).stem
    return int(name)

teamPreifixes = ['Home', 'Visiting']
mainKeys = [
    'Year',
    'GameSno',
    'HomeTeamName',
    'VisitingTeamName',
    'HomeTotalScore',
    'VisitingTotalScore',
]
calcKeys = [
    'HittingCnt',
    'ErrorCnt',
]

header = mainKeys.copy()
for teamPrefix in teamPreifixes:
    for key in calcKeys:
        header.append(teamPrefix + key)
header.append('InningCnt')

rows = []

years = os.listdir('data')
for year in years:
    dirname = 'data/' + year
    gameFiles = os.listdir(dirname)
    gameFiles.sort(key = sortGameFile)
    for gameFile in gameFiles:
        f = open(dirname + '/' + gameFile, encoding='utf-8')
        # returns JSON object as
        # a dictionary
        data = json.load(f)
        row = []
        for key in mainKeys:
            row.append(data['CurtGameDetailJson'][key])
        for teamPrefix in teamPreifixes:
            teamName = data['CurtGameDetailJson'][teamPrefix + 'TeamName']
            for key in calcKeys:
                calcStat = getTeamStat(data['ScoreboardJson'], teamName, key)
                row.append(calcStat)

        row.append(data['ScoreboardJson'][0]['InningSeq'])
        rows.append(row)

# print(len(rows))
with open('GameStats.csv', 'w', newline='', encoding='utf-8') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(header)
    write.writerows(rows)