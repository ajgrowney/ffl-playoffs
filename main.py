import sys
import pandas as pd
import numpy as np
from functions import scrape_game_url, scrape_week_url, stats_to_dataframe



def form_year_week_url(year, week):
    return ("https://www.pro-football-reference.com/years/"+str(year)+"/week_"+str(week)+".htm")

def form_csv_path(year, week,stat):
    return("data-"+str(year)+"/"+str(year)+"-"+stat+"-week-"+str(week)+".csv")


if len(sys.argv) == 1: print("Need parameter: [game, week, year, games_in_week]")
elif sys.argv[1] == "game": 
    game_url = sys.argv[2] if len(sys.argv) == 3 else "https://www.pro-football-reference.com/boxscores/201909220kan.htm"
    # current_week_pass_df = pd.read_csv("data-2019/2019-passing-week-1.csv")
    game = (scrape_game_url(game_url))
    print(game.receiving_categories, game.receiving_data)
    # game_pass_df = stats_to_dataframe(game.passing_data, game.passing_categories, "passing", 1,2019)
    # game_rush_df = stats_to_dataframe(game.rushing_data, game.rushing_categories, "rushing", 1,2019)
    # game_receiving_df = stats_to_dataframe(game.receiving_data, game.receiving_categories, "receiving", 1,2019)
    # current_week_pass_df = pd.concat([current_week_pass_df,game_pass_df], ignore_index=True).drop_duplicates().reset_index(drop=True)
    # print(current_week_pass_df)

elif sys.argv[1] == "week":
    week, year = sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else 2019
    
    game_urls = ["http://www.pro-football-reference.com/"+u for u in scrape_week_url(form_year_week_url(year,week))]
    current_week_pass_df = pd.read_csv(form_csv_path(year,week,"passing"))
    current_week_rush_df = pd.read_csv(form_csv_path(year,week,"rushing"))
    current_week_receiving_df = pd.read_csv(form_csv_path(year,week,"receiving"))

    for game_url in game_urls:
        game = (scrape_game_url(game_url))
        game_pass_df = stats_to_dataframe(game.passing_data, game.passing_categories, "passing", week, year)
        game_rush_df = stats_to_dataframe(game.rushing_data, game.rushing_categories, "rushing", week, year)
        game_receiving_df = stats_to_dataframe(game.receiving_data, game.receiving_categories, "receiving", week, year)
        current_week_pass_df = pd.concat([current_week_pass_df,game_pass_df], ignore_index=True).drop_duplicates().reset_index(drop=True)
        current_week_rush_df = pd.concat([current_week_rush_df,game_rush_df], ignore_index=True).drop_duplicates().reset_index(drop=True)
        current_week_receiving_df = pd.concat([current_week_receiving_df,game_receiving_df], ignore_index=True).drop_duplicates().reset_index(drop=True)

    current_week_pass_df.to_csv(form_csv_path(year,week,"passing"),index=False)
    current_week_rush_df.to_csv(form_csv_path(year,week,"rushing"),index=False)
    current_week_receiving_df.to_csv(form_csv_path(year,week,"receiving"),index=False)


elif sys.argv[1] == "year": print(scrape_week_url(form_year_week_url(2019,2)))


