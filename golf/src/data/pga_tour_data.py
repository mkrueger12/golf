import json

import pandas as pd
import requests

from golf.src.functions import get_user_key

# get players table
url = 'https://statdata.pgatour.com/players/player.json?userTrackingId=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjQxNDIxOTEsIm5iZiI6MTY2NDE0MjE5MSwiZXhwIjoxNjY0MTQzOTkxfQ.tiBDggyR7nuPki_ZcexFhMD-AKZZy7friUqI_ZS8zpQ'

df = requests.get(url).json()
players = pd.DataFrame(df['plrs'])
players = players[['pid', 'playedYrs']]

players = players.explode('playedYrs').reset_index(drop=True) #explode playedYrs column

players['playedYrs'] = players['playedYrs'].astype(int) #convert playedYrs to int

players = players[players['playedYrs'] > 2012] #filter for players who have played since 2018

players = list(players['pid'].unique())

# read in tournament data
tournaments = pd.read_csv('tournaments.csv')
tournaments = list(tournaments['tournament'])

# get player history
id = get_user_key()
data = []

for p in players:

    url = f'https://statdata-api-prod.pgatour.com/api/clientfile/PlayerTournamentHistoryRef?P_ID={p}&format=json&userTrackingId={id}'
    print(p, requests.get(url).status_code, url)
    r = requests.get(url).content
    r = json.loads(r)

    df = pd.DataFrame(r)
    df = pd.json_normalize(r['years'],  'tournaments',  ['year'])
    df['pid'] = p
    data.append(df)

data = pd.concat(data)
data.to_csv('golf/data/interim/player_history.csv', index=False)





