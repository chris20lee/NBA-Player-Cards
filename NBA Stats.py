#Imports
from bs4 import BeautifulSoup
import pandas as pd
from random import randint
from requests import get
from time import sleep
from warnings import warn

# Variables
DATA_DIR = '/Users/chrislee/PyCharmProjects/NBA-Player-Cards'
START_YEAR = 2022
END_YEAR = 2025
STAT_TYPES = ['per_poss', 'advanced']

# Functions
def get_html(url):
    try:
        response = get(url, timeout=5)
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

# Get current salaries for players on each team
def get_salaries(teams_list):
    salaries = []
    # Loop through the teams
    for team in teams_list:
        # Slow down the web scrape
        sleep(randint(1, 4))
        url = 'https://www.basketball-reference.com/contracts/{}.html'.format(team)
        try:
            response = get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')

            rows = soup.find('tbody').find_all('tr')
            for i in range(len(rows)):
                player_id = [a['href'] for a in rows[i].find_all('a', href=True) if a.text]
                sal = [a.text for a in rows[i].find_all('td')]
                season = [i.text for i in soup.find_all('tr')[1].find_all('th')][2]
                season_short = season[2:5] + season[-2:]
                if len(sal) == 1:
                    sal.append('$0')
                if len(player_id) == 0:
                    player_id = ['blank']
                salaries.append([player_id[0], sal[1], team, season_short])
                # salaries.append([player_id[0], sal[1], get_image_url(player_id[0])])
                # print('  Completed {}'.format(player_id[0]))

            print('{} added to salary table'.format(team))

        except:
            pass

        # Warning for non-200 status codes
        if response.status_code != 200:
            warn('Error: Status code {}'.format(response.status_code))

    return salaries

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

        print('{} completed for {} table'.format(year, stat_type))

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

    # Save to csv
    player_stats.to_csv('{}/Data/nba_player_stats_{}.csv'.format(DATA_DIR, stat_type), index=False)

########################################################################################################################
# FIX ENCODING
########################################################################################################################
# Read all stats into their own variables
per_poss = pd.read_csv('{}/Data/nba_player_stats_per_poss.csv'.format(DATA_DIR), encoding='utf-8')
advanced = pd.read_csv('{}/Data/nba_player_stats_advanced.csv'.format(DATA_DIR), encoding='utf-8')

# Merge per game stats into total stats table
all_data = per_poss.merge(advanced, on=['player', 'age', 'team', 'pos', 'g', 'gs', 'mp', 'year', 'season', 'player_id']
                          , how='inner')
all_data.columns = all_data.columns.str.replace('_x', '')

# Drop league average rows
all_data = all_data.loc[all_data['rk'] != 0]

########################################################################################################################
# MOVE THIS PART TO LATER
########################################################################################################################
# Remove players who got traded and keep the aggregated stats
all_data['count'] = all_data.groupby(['year', 'season', 'player_id']).cumcount()
all_data = all_data.loc[all_data['count'] == 0]

# Drop unused columns
all_data = all_data.drop(['rk', 'g', 'gs', 'mp', 'fg', 'fga', 'fg_percent', '3p', '3pa', '3p_percent', '2p', '2pa',
                          '2p_percent', 'efg_percent', 'ft', 'fta', 'ft_percent', 'orb', 'drb', 'trb', 'ast', 'stl',
                          'blk', 'tov', 'pf', 'pts', 'awards', 'rk_y', '3par', 'ftr', 'orb_percent', 'drb_percent',
                          'trb_percent', 'ast_percent', 'stl_percent', 'blk_percent', 'tov_percent', 'usg_percent',
                          'ws_48', 'awards_y', 'count'], axis=1)

########################################################################################################################
# FIX ENCODING
########################################################################################################################
all_data.apply(lambda x: pd.api.types.infer_dtype(x.values))

# Save csv
all_data.to_csv('{}/Data/nba_player_stats_combined.csv'.format(DATA_DIR), index=False)
print('Combined NBA player stats table completed for {}-{}'.format(START_YEAR, END_YEAR))


teams = all_data['team'].unique()
teams = [team for team in teams if not any(char.isdigit() for char in team)]
teams = sorted(teams)
# teams = teams[27:30]
# print(teams)

salaries = get_salaries(teams)

salaries = pd.DataFrame(salaries, columns=['player_id', 'salary', 'team', 'season'])
# salaries = pd.DataFrame(salaries, columns=['player_id', 'salary', 'image_url'])

# Drop blank rows
salaries = salaries.loc[salaries['player_id'] != 'blank']

salaries = salaries.replace('', '$0')

salaries.to_csv('{}/Data/nba_player_salaries.csv'.format(DATA_DIR), index=False)