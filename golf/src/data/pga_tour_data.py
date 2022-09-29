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
tournaments = tournaments['tournament']

a = get_user_key()

