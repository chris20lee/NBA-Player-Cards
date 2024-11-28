# https://jfresh.substack.com/p/2022-nhl-player-cards-explainer

# https://github.com/xbeat/Machine-Learning/blob/main/Advantages%20of%20Weighted%20Averaging%20in%20Ensemble%20Models.md

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
from matplotlib.ticker import MaxNLocator
import requests
from PIL import Image
from io import BytesIO

DATA_DIR = '/Users/chrislee/PyCharmProjects/NBA-Player-Cards'
data = pd.read_csv('{}/Data/nba_player_stats_combined.csv'.format(DATA_DIR), encoding='utf-8')

player = 'LeBron James'
year = 2024

cols_dict = {'ortg':True, 'drtg':False, 'per':True, 'ts_percent':True, 'ows':True, 'dws':True, 'ws':True, 'obpm':True,
             'dbpm':True, 'bpm':True, 'vorp':True}
for k, v in cols_dict.items():
    data['{}_perc_rk'.format(k)] = data.groupby(['year', 'season'])[k].rank(pct=True, ascending=v)

# ref_player = data.loc[data['player'] == player]
ref_player = data.loc[(data['player'] == player) & (data['year'] <= year) & (data['year'] >= year - 2)]
print(ref_player)

########################################################################################################################
# Make Subplot
########################################################################################################################

player_id = ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['player_id'].values[0]

url = 'https://www.basketball-reference.com/players/b/barnesc01.html'
# url = 'https://www.basketball-reference.{}'.format(player_id)
print(url)

# Create a new figure
fig = plt.figure(figsize=(9, 6))

# Add a plot at a specific location: [left, bottom, width, height]
# Coordinates are in figure-relative units (0 to 1)

ax0 = fig.add_axes([0.03, 0.03, 0.61, 0.94])

response = get(url, timeout=5)
soup = BeautifulSoup(response.text, 'html.parser')

# Warning for non-200 status codes
if response.status_code != 200:
    warn('Error: Status code {}'.format(response.status_code))

# Get player picture url
x = soup.find_all('img')[1].get('src')
url = x
print(url)

# Fetch the image using requests
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Open the image using PIL
    img = Image.open(BytesIO(response.content))

    print(img.size)

    width, height = img.size
    aspect_ratio = width / height
    new_width = 200  # Set new width
    new_height = int(new_width / aspect_ratio)  # Maintain aspect ratio

    # Resize with new dimensions
    img_resized = img.resize((new_width, new_height))

    print(img_resized.size)

    # Convert image to numpy array
    # img_array = np.array(img)

    # Display the image using matplotlib
    ax0.imshow(img_resized)
    ax0.axis('off')  # Hide axes
    # ax0.show()
else:
    print("Failed to retrieve the image.")

ax0.text(0, 1, player, fontdict={'fontsize': 20, 'fontweight': 'bold'}, ha='left', va='top')
ax0.text(0.4, 0.85, 'Proj. WS %', fontdict={'fontsize': 10, 'fontstyle': 'italic'}, ha='center', va='center')

ax0.text(0.6, 0.85, 'Proj. WS %', fontdict={'fontsize': 10, 'fontstyle': 'italic'}, ha='center', va='center')
ax0.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
ax0.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
for pos in ['right', 'top', 'left', 'bottom']:
    ax0.spines[pos].set_visible(False)

# WS Percentile Timeline
ax1 = fig.add_axes([0.67, 0.6, 0.3, 0.3])
ref_player.plot(ax=ax1, kind='line', x='season', y='ws_perc_rk', marker='o', markersize=5, color='r', linewidth=2.5,
                legend=None).grid(axis='y')
ax1.set_title('WS Percentile Timeline', fontdict={'fontsize': 12, 'fontweight': 'bold'})
ax1.set_xlabel('')
ax1.set_ylabel('')
ax1.set_ylim(0, 1)
ax1.get_yaxis().set_major_formatter(PercentFormatter(1))
ax1.margins(x=0.2)
ax1.tick_params(axis='both', labelsize=8)
ax1.yaxis.set_major_locator(MaxNLocator(nbins=4))
ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
ax1.tick_params(axis='y', which='both', right=False, left=False, labelleft=True)
for pos in ['right', 'top', 'left']:
    ax1.spines[pos].set_visible(False)

# Off Rating vs Def Rating Graph
ax2 = fig.add_axes([0.67, 0.15, 0.3, 0.3])
ref_player.plot(ax=ax2, kind='line', x='season', y=['ortg_perc_rk', 'drtg_perc_rk'], marker='o', markersize=5,
                color=['b', 'r'], linewidth=2.5, legend=None).grid(axis='y')
ax2.set_title('Off Rating vs Def Rating', fontdict={'fontsize': 12, 'fontweight': 'bold'})
ax2.set_xlabel('')
ax2.set_ylabel('')
ax2.set_ylim(0, 1)
ax2.get_yaxis().set_major_formatter(PercentFormatter(1))
ax2.margins(x=0.2)
ax2.tick_params(axis='both', labelsize=8)
ax2.yaxis.set_major_locator(MaxNLocator(nbins=4))
ax2.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
ax2.tick_params(axis='y', which='both', right=False, left=False, labelleft=True)
for pos in ['right', 'top', 'left']:
    ax2.spines[pos].set_visible(False)

plt.show()