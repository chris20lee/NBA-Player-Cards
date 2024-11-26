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

# header = [i.text for i in soup.find_all('tr')[0].find_all('th')]
# header.append('Year')
# header = header[1:]  # Drop rank column
# header = [item.replace('%', '_percent').replace('/', '_').lower() for item in header]
# # print(header)
# # num_cols = len(header)
# # print(num_cols)
#
# rows = soup.find_all('tbody')[0].find_all('tr')
# for i in range(len(rows)):
#     player_id = [a['href'] for a in rows[i].find_all('td')[0].find_all('a', href=True) if a.text]
#     if len(player_id) != 0:
#         print(player_id[0][11:][:-5])
#     else:
#         print('league_average')

# Variables
draft_stats = pd.DataFrame()

# url = 'https://www.basketball-reference.com/players/b/barnesc01.html'
url = 'https://www.basketball-reference.com/contracts/TOR.html'
response = get(url, timeout=5)
soup = BeautifulSoup(response.text, 'html.parser')

# Warning for non-200 status codes
if response.status_code != 200:
    warn('Error: Status code {}'.format(response.status_code))

# Get player picture url
# x = soup.find_all('img')[1].get('src')
# print(x)
#
# url = x
#
# # Fetch the image using requests
# response = requests.get(url)
#
# # Check if the request was successful
# if response.status_code == 200:
#     # Open the image using PIL
#     img = Image.open(BytesIO(response.content))
#
#     # Convert image to numpy array
#     img_array = np.array(img)
#
#     # Display the image using matplotlib
#     plt.imshow(img_array)
#     plt.axis('off')  # Hide axes
#     plt.show()
# else:
#     print("Failed to retrieve the image.")

# for i in range(len(x)):
#     # print([a['href'] for a in x[i].find_all('td')[1].find_all('a', href=True) if a.text][0])
#     player_id = [a['href'] for a in x[i].find_all('td')[1].find_all('a', href=True) if a.text][0]
#     print(player_id[11:][:-5])

# Player ID and team ID
rows = soup.find('tbody').find_all('tr')
for i in range(len(rows)):
    player_id = [a['href'] for a in rows[i].find_all('a', href=True) if a.text]
    # salary = [b.text for b in rows[i].find_all('td') if b.text]
    # cur_salary = [c[1] if len(salary) >= 1 else '' for c in salary]
    # print(player_id, salary, cur_salary)
    x = rows[i].find_all('td')
    sal = [a.text for a in x]
    if len(sal) == 1:
        sal.append('$0')
    # print(player_id, sal)
    cur_sal = sal[1]
    print(player_id, cur_sal)
    # if len(player_id) != 0:
    #     clean_id = player_id[0][11:][:-5]
    # else:
    #     clean_id = 'league_average'
    # stats.append([j.text for j in rows[i] if j.text != ' '])
# x = soup.find_all(class_= 'salary-tm')
# # print(x)
# for i in range(len(x)):
#     # print(i)
#     print(x[i].text)
    # y = x[i].find_all('tr')
    # for j in range(len(y)):
    #     print(y[j].text)

# print(soup.find('div').find('td'))

# print(soup.find_all('tbody')[0].find_all('tr', class_=None)[0].find_all('td')[1])
# print(soup.find_all('tbody')[0].find_all('tr', class_=None)[0].find_all(attrs={'class': 'left'}))
# print(soup.find_all('tbody')[0].find_all('tr', class_=None)[0].find_all('a'))

x =[]
if not x:
    print('ji')