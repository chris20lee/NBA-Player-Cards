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
import requests
from PIL import Image
from io import BytesIO

DATA_DIR = '/Users/chrislee/PyCharmProjects/NBA-Player-Cards'
data = pd.read_csv('{}/Data/nba_player_stats_combined.csv'.format(DATA_DIR), encoding='utf-8')

player = 'Klay Thompson'

def percentile_rank(col):
    data['{}_perc_rk'.format(col)] = data.groupby(['year', 'season'])[col].rank(pct=True)

# Compute percentile ranks
con_cols = ['ortg', 'drtg', 'per', 'ts_percent', 'ows', 'dws', 'ws', 'obpm', 'dbpm', 'bpm', 'vorp']
for i in con_cols:
    percentile_rank(i)

print(data.loc[data['player'] == player])

ref_player = data.loc[data['player'] == player]
cols = ref_player[['season', 'ortg_perc_rk', 'drtg_perc_rk']]

ref_player.plot(kind='line', x='season', y='ws_perc_rk', marker='o', color='r', linewidth=3.5, legend=None).grid(axis='y')
# cols.plot(kind='line', x='season', marker='o', color=['b', 'r'], linewidth=3.5, legend=None).grid(axis='y')
plt.gcf().set_size_inches(6, 4)
plt.title('Win Shares Percentile Rank', fontdict={'fontsize': 15, 'fontweight': 'bold'})
plt.xlabel('')
plt.ylabel('')
plt.xticks(fontsize=9)
plt.yticks(fontsize=9)
plt.ylim(0, 1)
# plt.grid(True)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.tight_layout()
plt.show()
# plt.savefig('{}/{} in {}.png'.format(DATA_DIR, title, country), dpi=dpi_fig)
plt.close()
