# https://jfresh.substack.com/p/2022-nhl-player-cards-explainer

#Imports
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np
import pandas as pd
from random import randint
from requests import get
from time import sleep
from warnings import warn
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO

# WS
# PER
# TS%
# USG%
# OWS
# DWS
# OBPM
# DBPM
# BPM
# VORP
# ORtg
# DRtg

# Variables
DATA_DIR = '/Users/chrislee/PyCharmProjects/NBA-Player-Cards'

# Read all stats into their own variables
data = pd.read_csv('{}/Data/combined_nba_player_stats.csv'.format(DATA_DIR), encoding='utf-8')
# print(data)

teams = data['team'].unique()
teams = teams[0:3]
print(teams)

for team in teams:
    sleep(randint(1, 4))
    url = 'https://www.basketball-reference.com/contracts/{}.html'.format(team)
    try:
        response = get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        pass
    print(team, url)
    # Warning for non-200 status codes
    if response.status_code != 200:
        warn('Error: Status code {}'.format(response.status_code))
        # print('error')
    else:
        print(team, url)

    # # Player ID and team ID
    # rows = soup.find('tbody').find_all('tr')
    # for i in range(len(rows)):
    #     player_id = [a['href'] for a in rows[i].find_all('a', href=True) if a.text]
    #     x = rows[i].find_all('td')
    #     sal = [a.text for a in x]
    #     if len(sal) == 1:
    #         sal.append('$0')
    #     cur_sal = sal[1]
    #     print(player_id, cur_sal)