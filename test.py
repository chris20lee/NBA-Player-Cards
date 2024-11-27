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


# url = 'https://www.basketball-reference.com/players/b/barnesc01.html'
url = 'https://www.basketball-reference.com/contracts/TOR.html'
response = get(url, timeout=5)
soup = BeautifulSoup(response.text, 'html.parser')

# Warning for non-200 status codes
if response.status_code != 200:
    warn('Error: Status code {}'.format(response.status_code))

# # Get player picture url
# x = soup.find_all('img')[1].get('src')
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

# Player ID and team ID
rows = soup.find('tbody').find_all('tr')
print(len(rows))
for i in range(len(rows)):
    x = rows[i].find_all('a', href=True)
    player_id = [a['href'] for a in x if a.text]
    sal = [a.text for a in rows[i].find_all('td')]
    if len(sal) == 1:
        sal.append('')
    if len(player_id) == 0:
        player_id = ['blank']
    print(player_id[0], sal[1])
    # print(player_id, sal)