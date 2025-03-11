from nba_stat_scraper import scrape_team_year
from twok_ratings_scraper import format_player_name, scrape_2k_data, save_to_csv, scrape_players
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures
import threading
import csv

# Global lock for thread-safe updates to shared lists
lock = threading.Lock()

def main():
    nba_teams = ['ATL', 'BRK','BOS', 'NJN' 'CHA', 'CHI', 'CHO', 'CLE', 'DET', 'IND', 'MIA', 'MIL',
                 'NYK', 'ORL', 'PHI', 'TOR', 'WAS', 'DAL', 'DEN', 'GSW', 'HOU', 'LAC', 
                 'LAL', 'MEM', 'MIN', 'NOP', 'NOH', 'OKC', 'PHO', 'POR', 'SAC', 'SAS', 'UTA']

    years = range(2010, 2026)

    all_per_game_data = []
    all_per_game_data_post = []
    all_pbp_data = []
    all_pbp_data_post = []

    # Scrape NBA stats
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scrape_team_year, team, year, all_per_game_data, all_per_game_data_post, all_pbp_data, all_pbp_data_post) 
                   for team in nba_teams for year in years]
        concurrent.futures.wait(futures)

    # Convert lists of dictionaries to DataFrames
    df_per_game = pd.DataFrame(all_per_game_data)
    df_pbp = pd.DataFrame(all_pbp_data)
    df_per_game_post = pd.DataFrame(all_per_game_data_post)
    df_pbp_post = pd.DataFrame(all_pbp_data_post)

    # Merge DataFrames and save to CSV
    df_nba = merge_dataframes(df_per_game, df_pbp, df_per_game_post, df_pbp_post)

    # Scrape 2K ratings
    df_nba['name_slug'] = df_nba['name'].apply(format_player_name)
    player_slugs = df_nba['name_slug'].unique().tolist()
    scrape_players(player_slugs)

    # Load 2K ratings data
    df_2k = pd.read_csv("2k_ratings_wingspan_height.csv")

    # Extract year from 2K ratings data
    def extract_year(twok_string):
        try:
            # Extract the last two characters and convert to int
            year_suffix = int(twok_string[-2:])
            # Determine the full year, assuming NBA 2K00 corresponds to 1999
            year = 2000 + year_suffix if year_suffix >= 5 else 1900 + year_suffix
            return year - 1  # Subtract 1 from the extracted year
        except ValueError:
            return None  # Handle unexpected values gracefully

    df_2k['year'] = df_2k['twok_year'].apply(extract_year)

    # Merge NBA stats with 2K ratings
    df_2k_nba = df_nba.merge(df_2k, on=['year', 'name_slug'], how='left')

    # Save the updated DataFrame
    df_2k_nba.to_csv('nba_combined_stats_with_slugs.csv', index=False)
    print("Combined data saved to 'nba_combined_stats_with_slugs.csv'")

def merge_dataframes(df_per_game, df_pbp, df_per_game_post, df_pbp_post):
    # Merge DataFrames on Player Name and Year
    df_combined = df_per_game.merge(df_per_game_post, on=['team', 'year', 'name'], how='left') \
                            .merge(df_pbp, on=['team', 'year', 'name'], how='left') \
                            .merge(df_pbp_post, on=['team', 'year', 'name'], how='left')
    df_combined['team'] = df_combined['team'].replace({
        'CHO': 'CHA',
        'NJN': 'BRK',
        'NOP': 'NOH'
    })
    # Export combined DataFrame to CSV
    df_combined.to_csv('nba_combined_stats.csv', index=False)
    print('NBA stats scraping complete and saved to nba_combined_stats.csv')
    return df_combined

if __name__ == "__main__":
    main()