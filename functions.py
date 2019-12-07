
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

class GameObject:
    # Param { ResultSet } stats_tables - containing all the tables needed for Game data
    # Param { Dictionary } table_ids - keys: [rushing, passing, receiving], values: id used by pro-football-refs
    def __init__(self, stat_tables, table_ids):
        for table in stat_tables:
            if table['id'] == table_ids['passing']: self.passing_categories, self.passing_data = scrape_data_table(table,"passing")
            elif table['id'] == table_ids['rushing']: self.rushing_categories, self.rushing_data = scrape_data_table(table,"rushing")
            elif table['id'] == table_ids['receiving']: self.receiving_categories, self.receiving_data = scrape_data_table(table,"receiving")

# Param: { Dictionary } stats_dict - dictionary containing all stats for a week
# Param: { List<String> } stat_categories - list of columns for the dataframe
# Param: { String } stat_category_name - category of the stats (e.g. "rushing", "receiving", "passing")
# Param: { Int } stat_week - week the stats happened (e.g. 2019)
# Param: { Int } stat_year - year the stats happened (e.g. 1)
# Return: { Pandas.DataFrame } - Dataframe that will be written to and read from csv formats in the data folders
def stats_to_dataframe(stats_dict: dict, stat_categories: list, stat_category_name: str, stat_week: int, stat_year: int):
    df = pd.DataFrame.from_dict(stats_dict,orient='index')
    return df

# Return: { List } table_stats - List of all the statistics recorded in the table
# Return: { Dictionary } player_stats - Dictionary of objects holding each players stats from the game
def scrape_data_table(data_table, category):
    table_stats, player_stats = [], {}
    
    # Table Headers: List of all stats being recorded
    header = data_table.find('thead')
    
    # If it is a rushing, passing, or receiving table, scraping player_ids
    if(category == "rushing" or category == "passing" or category == "receiving"): table_stats.append("player_id")

    for data_row in header.find_all('th'):
        table_stats.append(data_row['data-stat'])

    # Table Rows: For each player, create Player object and add their game stats to the object
    body = data_table.find('tbody')
    player_rows = body.find_all('tr',attrs={'class': None})
    for player in player_rows:
        player_id, stats = "", {}

        # Fill Player's ID and Stats
        for data_row in player:
            if data_row['data-stat'] == 'player':
                player_id, name = data_row['data-append-csv'], data_row.find('a').text
                stats[data_row['data-stat']] = data_row.text
                stats['player_id'] = player_id
            else:
                stats[data_row['data-stat']] = data_row.text
        
        # Write Player Stats to Dictionary
        player_stats[player_id] = stats
    
    return table_stats, player_stats


# Param: { String } url - pro-football-reference url for a game
# Return: { GameObject }  game - holds the game data from that url
def scrape_game_url(url):
    table_ids = {
        "passing": "passing_advanced",
        "rushing": "rushing_advanced",
        "receiving": "receiving_advanced"
    }
    response = requests.get(url)
    html = response.text
    
    # Clean HTML for scraping
    html = html.replace('<!--','').replace('-->','')
    SoupObject = BeautifulSoup(html,"html.parser")
    
    category_tables = SoupObject.find_all('table', {"id": list(table_ids.values())})
    game = GameObject(category_tables, table_ids)
    return game



# Param: { String } - url to scrape for the week's boxscores
# Return: { List<String> } - list of urls formed as '/boxscores/{gameid}'
def scrape_week_url(url):
    response = requests.get(url)
    html = response.text

    WeekSoup = BeautifulSoup(html,"html.parser")
    game_summaries = WeekSoup.find('div', {'class': "game_summaries"}).find_all('div',{'class': "game_summary"})
    game_urls = [(u.find('a', attrs={'href': re.compile("/boxscores.*")})['href']) for u in game_summaries]
    return game_urls
