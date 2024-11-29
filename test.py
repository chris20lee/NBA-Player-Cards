#Imports
from bs4 import BeautifulSoup
import pandas as pd
from random import randint
from requests import get
from time import sleep
from warnings import warn
import ftfy
from unidecode import unidecode

# Variables
DATA_DIR = '/Users/chrislee/PyCharmProjects/NBA-Player-Cards'
START_YEAR = 2025
END_YEAR = 2025
STAT_TYPES = ['per_poss']

# Functions
def get_html(url):
    try:
        response = get(url, timeout=5)
        # response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        soup = ''

    # Warning for non-200 status codes
    if response.status_code != 200:
        warn('Error: Status code {}'.format(response.status_code))

    return soup

# Get variable headers for the statistics from the page
def get_header(soup):
    header = [i.text for i in soup.find_all('tr')[0].find_all('th')]
    header.extend(['year', 'season', 'player_id'])
    header = [item.replace('%', '_percent').replace('/', '_').lower() for item in header]
    return header

# Get the player statistics for the stat type
def get_stats(soup, headers, year):
    stats = []
    season = (str(year - 1))[-2:] + '-' + (str(year))[-2:]
    rows = soup.find_all('tbody')[0].find_all('tr')
    for i in range(len(rows)):
        player_id = [a['href'] for a in rows[i].find_all('td')[0].find_all('a', href=True) if a.text]
        stats.append([j.text for j in rows[i] if j.text != ' '])
        if len(player_id) == 0:
            player_id = ['']
        stats[i].extend([year, season, player_id[0]])

    stats = pd.DataFrame(stats, columns=headers)
    return stats

# Main loop to get player statistics for all stat types for years of interest
for stat_type in STAT_TYPES:
    player_stats = pd.DataFrame()
    # Loop through the years
    for year in range(START_YEAR, END_YEAR + 1):
        # Slow down the web scrape
        sleep(randint(1, 4))

        # Get website
        url = ('https://www.basketball-reference.com/leagues/NBA_{}_{}.html'.format(year, stat_type))
        html_soup = get_html(url)

        # Get header
        if year == START_YEAR:
            headers = get_header(html_soup)

        player_stats = pd.concat([player_stats, pd.DataFrame(get_stats(html_soup, headers, year))]
                                 , ignore_index=True)

        print('  {} completed for {} table'.format(year, stat_type))

    player_stats = player_stats.copy()

    # Drop empty columns
    drop_cols = []
    for col in player_stats.columns:
        if (len(col) <= 1) and (col != 'g'):
            drop_cols.append(col)
    player_stats = player_stats.drop(columns=drop_cols)

    # Convert numerical columns to numeric
    cols = [i for i in player_stats.columns if i not in ['player', 'pos', 'team', 'awards', 'season', 'player_id']]
    for col in cols:
        player_stats[col] = pd.to_numeric(player_stats[col])

    # Fill blanks
    player_stats = player_stats.fillna(0)

player_stats['fixed_name'] = player_stats.apply(lambda x: ftfy.fix_text(x['player']), axis=1)

player_stats.to_csv('{}/Data/test.csv'.format(DATA_DIR), index=False)

ref_player = player_stats[player_stats['player_id'] == '/players/j/jokicni01.html']['player'].values[0]

# print(ref_player)

print(ftfy.fix_text(ref_player))

print(unidecode(ref_player))