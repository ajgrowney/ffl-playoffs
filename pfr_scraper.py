
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup


class GameObject:

    # Param: stats_tables { ResultSet } - containing all the tables needed for Game data
    # Param: table_ids { Dictionary } - keys: [rushing, passing, receiving], values: id used by pro-football-refs
    # Param: teams_abbrev { Set } - Two teams abbreviations playing in the game
    def __init__(self, stat_tables, table_ids, teams_abbrev):
        for table in stat_tables:
            if table['id'] == table_ids['passing']: 
                self.passing_categories, self.passing_data = scrape_data_table(table,"passing", teams_abbrev)
            elif table['id'] == table_ids['rushing']: 
                self.rushing_categories, self.rushing_data = scrape_data_table(table,"rushing", teams_abbrev)
            elif table['id'] == table_ids['receiving']: 
                self.receiving_categories, self.receiving_data = scrape_data_table(table,"receiving", teams_abbrev)


# Param: stats_dict { Dictionary } - dictionary containing all stats for a week
# Param: stat_categories { List<String> } - list of columns for the dataframe
# Param: stat_category_name { String } - category of the stats (e.g. "rushing", "receiving", "passing")
# Param: stat_week { Int } - week the stats happened (e.g. 2019)
# Param: stat_year { Int } - year the stats happened (e.g. 1)
# Return: { Pandas.DataFrame } - Dataframe that will be written to and read from csv formats in the data folders
def stats_to_dataframe(stats_dict: dict, stat_categories: list, stat_category_name: str, stat_week: int, stat_year: int):
    df = pd.DataFrame.from_dict(stats_dict,orient='index')
    return df

# Return: table_stats { List } - List of all the statistics recorded in the table
# Return: player_stats { Dictionary } - Dictionary of objects holding each players stats from the game
def scrape_data_table(data_table, category, teams):
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

        # Fill Player's ID, Opponent, and Stats
        for data_row in player:
            stats[data_row['data-stat']] = data_row.text

            if data_row['data-stat'] == 'player':
                player_id, name = data_row['data-append-csv'], data_row.find('a').text
                stats['player_id'] = player_id
            
            elif data_row['data-stat'] == 'team':
                opponent = teams - set([ stats[data_row['data-stat']]])
                stats['opponent'] = opponent.pop()               
        
        # Write Player Stats to Dictionary
        player_stats[player_id] = stats
    
    return table_stats, player_stats


# Param: url { String } - pro-football-reference url for a game
# Return: { GameObject } - holds the game data from that url
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
    
    table_ids = {
        "passing": "passing_advanced",
        "rushing": "rushing_advanced",
        "receiving": "receiving_advanced"
    }
    category_tables = SoupObject.find_all('table', {"id": list(table_ids.values())})
    teams_container = SoupObject.find('table', {'id': "team_stats"})
    home_team = teams_container.find('th', {"data-stat": "home_stat"}).text
    road_team = teams_container.find('th', {"data-stat": "vis_stat"}).text
    teams = set([home_team,road_team])
    # Special way to grab teams from the scorebox of their pages
    game = GameObject(category_tables, table_ids, teams)
    return game



# Param: url { String } - to scrape for the week's boxscores
# Return: { List<String> } - list of urls formed as '/boxscores/{gameid}'
def scrape_week_url(url):
    response = requests.get(url)
    html = response.text

    WeekSoup = BeautifulSoup(html,"html.parser")
    game_summaries = WeekSoup.find('div', {'class': "game_summaries"}).find_all('div',{'class': "game_summary"})
    game_urls = [(u.find('a', attrs={'href': re.compile("/boxscores.*")})['href']) for u in game_summaries]
    return game_urls
