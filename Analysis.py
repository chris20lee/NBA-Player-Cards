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
stats = pd.read_csv('{}/Data/nba_player_stats_combined.csv'.format(DATA_DIR), encoding='utf-8')
salaries = pd.read_csv('{}/Data/nba_player_salaries.csv'.format(DATA_DIR), encoding='utf-8')

data = stats.merge(salaries, on=['season', 'player_id'], how='left')
#
# data.to_csv('{}/Data/test.csv'.format(DATA_DIR), index=False)
#
# year = 2025
#
# ref_player = data.loc[(data['year'] == year) & (data['year'] >= year - 2)]
# print(ref_player)
#
# DATA_DIR = '/Users/chrislee/PyCharmProjects/NBA-Player-Cards'
# data = pd.read_csv('{}/Data/nba_player_stats_combined.csv'.format(DATA_DIR), encoding='utf-8')

player = 'LeBron James'
year = 2025

def colour_scale(value):
    # Blue scale if in top half
    if value >= 50:
        start = np.array([0.9, 0.9, 0.9])
        stop = np.array([0, 0.6, 1])
        spot = value - 50
    # Red scale if in bottom half
    else:
        start = np.array([1, 0.4, 0.4])
        stop = np.array([0.9, 0.9, 0.9])
        spot = value

    # Create a linear interpolation between the two colors
    colours = np.linspace(start, stop, 51)

    return colours[spot]

cols_dict = {'ortg':True, 'drtg':False, 'per':True, 'ts_percent':True, 'ows':True, 'dws':True, 'ws':True, 'obpm':True,
             'dbpm':True, 'bpm':True, 'vorp':True}
for k, v in cols_dict.items():
    data['{}_perc_rk'.format(k)] = data.groupby(['year', 'season'])[k].rank(pct=True, ascending=v)

ref_player = data.loc[(data['player'] == player) & (data['year'] <= year) & (data['year'] >= year - 2)]
print(ref_player)

########################################################################################################################
# Make Subplot
########################################################################################################################

player_id = ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['player_id'].values[0]
player_position = ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['pos'].values[0]
player_age = ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['age'].values[0]
player_salary = ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['salary'].values[0]
player_ws = int(ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['ws_perc_rk'].values[0] * 100)
player_ows = int(ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['ows_perc_rk'].values[0] * 100)
player_dws = int(ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['dws_perc_rk'].values[0] * 100)
player_per = int(ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['per_perc_rk'].values[0] * 100)
player_ts_percent = int(ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['ts_percent_perc_rk'].values[0] * 100)
player_vorp = int(ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['vorp_perc_rk'].values[0] * 100)
player_obpm = int(ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['obpm_perc_rk'].values[0] * 100)
player_dbpm = int(ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['dbpm_perc_rk'].values[0] * 100)
player_bpm = int(ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['bpm_perc_rk'].values[0] * 100)
player_ortg = int(ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['ortg_perc_rk'].values[0] * 100)
player_drtg = int(ref_player[(ref_player['player'] == player) & (ref_player['year'] == year)]['drtg_perc_rk'].values[0] * 100)

url = 'https://www.basketball-reference.com{}'.format(player_id)
print(url)

# Create a new figure
fig = plt.figure(figsize=(8, 5))

# Add a plot at a specific location: [left, bottom, width, height]
# Coordinates are in figure-relative units (0 to 1)

ax0 = fig.add_axes([0.03, 0.03, 0.61, 0.94])
# Hard coded text
ax0.text(0, 1, player, fontdict={'fontsize': 22, 'fontweight': 'bold'}, ha='left', va='top')
ax0.text(0.45, 0.85, 'Proj. WS %', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='center', va='center')
ax0.text(0.7, 0.85, 'Pos:', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='right', va='center')
ax0.text(0.7, 0.77, 'Age:', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='right', va='center')
ax0.text(0.7, 0.69, 'MP:', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='right', va='center')
ax0.text(0.7, 0.61, 'Cap:', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='right', va='center')
ax0.text(0.1, 0.44, 'OWS', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='center', va='center')
ax0.text(0.28, 0.44, 'DWS', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='center', va='center')
ax0.text(0.46, 0.44, 'PER', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='center', va='center')
ax0.text(0.64, 0.44, 'TS %', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='center', va='center')
ax0.text(0.82, 0.44, 'VORP', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='center', va='center')
ax0.text(0.1, 0.24, 'OBPM', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='center', va='center')
ax0.text(0.28, 0.24, 'DBPM', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='center', va='center')
ax0.text(0.46, 0.24, 'BPM', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='center', va='center')
ax0.text(0.64, 0.24, 'ORtg', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='center', va='center')
ax0.text(0.82, 0.24, 'DRtg', fontdict={'fontsize': 12, 'fontstyle': 'italic'}, ha='center', va='center')

# Values
ax0.text(0.72, 0.85, player_position, fontdict={'fontsize': 12, 'fontweight': 'bold'}, ha='left', va='center')
ax0.text(0.72, 0.77, int(player_age), fontdict={'fontsize': 12, 'fontweight': 'bold'}, ha='left', va='center')
ax0.text(0.72, 0.69, 'Start/Bench', fontdict={'fontsize': 12, 'fontweight': 'bold'}, ha='left', va='center')
ax0.text(0.72, 0.61, player_salary, fontdict={'fontsize': 12, 'fontweight': 'bold'}, ha='left', va='center')
ax0.text(0.45, 0.7, '{}%'.format(player_ws),
         bbox=dict(facecolor=colour_scale(player_ws), edgecolor=colour_scale(player_ws), boxstyle='square,pad=0.6'),
         fontdict={'fontsize': 25, 'fontweight': 'bold'}, ha='center', va='center')
ax0.text(0.1, 0.36, '{}%'.format(player_ows),
         bbox=dict(facecolor=colour_scale(player_ows), edgecolor=colour_scale(player_ows), boxstyle='square,pad=0.5'),
         fontdict={'fontsize': 15, 'fontweight': 'bold'}, ha='center', va='center')
ax0.text(0.28, 0.36, '{}%'.format(player_dws),
         bbox=dict(facecolor=colour_scale(player_dws), edgecolor=colour_scale(player_dws), boxstyle='square,pad=0.5'),
         fontdict={'fontsize': 15, 'fontweight': 'bold'}, ha='center', va='center')
ax0.text(0.46, 0.36, '{}%'.format(player_per),
         bbox=dict(facecolor=colour_scale(player_per), edgecolor=colour_scale(player_per), boxstyle='square,pad=0.5'),
         fontdict={'fontsize': 15, 'fontweight': 'bold'}, ha='center', va='center')
ax0.text(0.64, 0.36, '{}%'.format(player_ts_percent),
         bbox=dict(facecolor=colour_scale(player_ts_percent), edgecolor=colour_scale(player_ts_percent),
                   boxstyle='square,pad=0.5'), fontdict={'fontsize': 15, 'fontweight': 'bold'}, ha='center',
         va='center')
ax0.text(0.82, 0.36, '{}%'.format(player_vorp),
         bbox=dict(facecolor=colour_scale(player_vorp), edgecolor=colour_scale(player_vorp), boxstyle='square,pad=0.5'),
         fontdict={'fontsize': 15, 'fontweight': 'bold'}, ha='center', va='center')
ax0.text(0.1, 0.16, '{}%'.format(player_obpm),
         bbox=dict(facecolor=colour_scale(player_obpm), edgecolor=colour_scale(player_obpm), boxstyle='square,pad=0.5'),
         fontdict={'fontsize': 15, 'fontweight': 'bold'}, ha='center', va='center')
ax0.text(0.28, 0.16, '{}%'.format(player_dbpm),
         bbox=dict(facecolor=colour_scale(player_dbpm), edgecolor=colour_scale(player_dbpm), boxstyle='square,pad=0.5'),
         fontdict={'fontsize': 15, 'fontweight': 'bold'}, ha='center', va='center')
ax0.text(0.46, 0.16, '{}%'.format(player_bpm),
         bbox=dict(facecolor=colour_scale(player_bpm), edgecolor=colour_scale(player_bpm), boxstyle='square,pad=0.5'),
         fontdict={'fontsize': 15, 'fontweight': 'bold'}, ha='center', va='center')
ax0.text(0.64, 0.16, '{}%'.format(player_ortg),
         bbox=dict(facecolor=colour_scale(player_ortg), edgecolor=colour_scale(player_ortg), boxstyle='square,pad=0.5'),
         fontdict={'fontsize': 15, 'fontweight': 'bold'}, ha='center', va='center')
ax0.text(0.82, 0.16, '{}%'.format(player_drtg),
         bbox=dict(facecolor=colour_scale(player_drtg), edgecolor=colour_scale(player_drtg), boxstyle='square,pad=0.5'),
         fontdict={'fontsize': 15, 'fontweight': 'bold'}, ha='center', va='center')

ax0.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
ax0.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
for pos in ['right', 'top', 'left', 'bottom']:
    ax0.spines[pos].set_visible(False)

ax00 = fig.add_axes([-0.01, 0.5, 0.25, 0.375])
response = get(url, timeout=5)
soup = BeautifulSoup(response.text, 'html.parser')
# Warning for non-200 status codes
if response.status_code != 200:
    warn('Error: Status code {}'.format(response.status_code))

# Fetch the image using requests
response = requests.get(soup.find_all('img')[1].get('src'))

# Check if the request was successful
if response.status_code == 200:
    # Open the image using PIL
    img = Image.open(BytesIO(response.content))
    # Display the image using matplotlib
    ax00.imshow(img)
    ax00.axis('off')  # Hide axes
    # ax0.show()
else:
    print("Failed to retrieve the image.")

# WS Percentile Timeline
ax1 = fig.add_axes([0.67, 0.6, 0.3, 0.3])
ref_player.plot(ax=ax1, kind='line', x='season', y='ws_perc_rk', marker='o', markersize=5, color=colour_scale(100), linewidth=2.5,
                legend=None).grid(axis='y')
ax1.set_title('WS Percentile Timeline', fontdict={'fontsize': 14, 'fontweight': 'bold'})
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
                color=[colour_scale(100), colour_scale(0)], linewidth=2.5, legend=None).grid(axis='y')
ax2.set_title('Off Rating vs Def Rating', fontdict={'fontsize': 14, 'fontweight': 'bold'})
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