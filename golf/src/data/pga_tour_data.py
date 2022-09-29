import requests
import pandas as pd
from golf.src.functions import get_user_key
import time
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# get players table
url = 'https://statdata.pgatour.com/players/player.json?userTrackingId=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjQxNDIxOTEsIm5iZiI6MTY2NDE0MjE5MSwiZXhwIjoxNjY0MTQzOTkxfQ.tiBDggyR7nuPki_ZcexFhMD-AKZZy7friUqI_ZS8zpQ'

df = requests.get(url).json()
players = pd.DataFrame(df['plrs'])
players = players[['pid', 'playedYrs']]

players = players.explode('playedYrs').reset_index(drop=True) #explode playedYrs column

players['playedYrs'] = players['playedYrs'].astype(int) #convert playedYrs to int

players = players[players['playedYrs'] > 2017] #filter for players who have played since 2018

players = list(players['pid'].unique())

# read in tournament data
tournaments = pd.read_csv('tournaments.csv')
tournaments = list(tournaments['tournament'])

# get shot data
for y in range(2018, 2023):
    id = get_user_key()

    for t in tournaments:
        data = []
        t = str(t).zfill(3)

        for p in players:
            url = f'https://statdata.pgatour.com/r/{t}/{y}/scorecards/{p}.json?userTrackingId={id}'
            print(requests.get(url).status_code, url)

            if requests.get(url).status_code == 200:

                r = requests.get(url).content
                r = json.loads(r)

                for i in range(len(r['p']['rnds'])):
                    df = pd.json_normalize(r['p']['rnds'][0], ['holes', ['shots']], max_level=1)

                    df['round'] = i + 1
                    df['tournament'] = t
                    df['year'] = y

                    data.append(df)

        data = pd.concat(data)
        data.to_csv(f'golf/data/interim/data/{y}_{t}.csv', index=False)




