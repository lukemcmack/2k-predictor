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

# Global lock for thread safety
lock = threading.Lock()

def scrape_team_year(team, year, all_per_game_data, all_per_game_data_post, all_pbp_data, all_pbp_data_post):
    options = Options()
    options.add_argument('--headless')  # Run Firefox in headless mode
    service = Service('geckodriver')
    driver = webdriver.Firefox(service=service, options=options)

    url = f'https://www.basketball-reference.com/teams/{team}/{year}.html'
    print(f'Accessing URL: {url}')
    driver.get(url)

    # Wait for the page to load completely
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, 'per_game_stats')))
    except Exception as e:
        print(f'Failed to load page for {team} {year}: {e}')
        driver.quit()
        return

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Scrape Per Game Stats
    per_game_table = soup.find('table', id='per_game_stats')
    if per_game_table:
        rows = per_game_table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            if not row.find('td', {'data-stat': 'name_display'}):
                continue
            cols = row.find_all(['th', 'td'])
            player_data = {
                'team': team,
                'year': year,
                'name': cols[1].text.strip(),
                'age': cols[2].text.strip(),
                'position': cols[3].text.strip(),
                'games': cols[4].text.strip(),
                'games_started': cols[5].text.strip(),
                'minutes_played_per_game': cols[6].text.strip(),
                'field_goals_per_game': cols[7].text.strip(),
                'field_goal_attempts_per_game': cols[8].text.strip(),
                'field_goal_percentage': cols[9].text.strip(),
                'three_point_field_goals_per_game': cols[10].text.strip(),
                'three_point_field_goal_attempts_per_game': cols[11].text.strip(),
                'three_point_field_goal_percentage': cols[12].text.strip(),
                'two_point_field_goals_per_game': cols[13].text.strip(),
                'two_point_field_goal_attempts_per_game': cols[14].text.strip(),
                'two_point_field_goal_percentage': cols[15].text.strip(),
                'effective_field_goal_percentage': cols[16].text.strip(),
                'free_throws_per_game': cols[17].text.strip(),
                'free_throw_attempts_per_game': cols[18].text.strip(),
                'free_throw_percentage': cols[19].text.strip(),
                'offensive_rebounds_per_game': cols[20].text.strip(),
                'defensive_rebounds_per_game': cols[21].text.strip(),
                'total_rebounds_per_game': cols[22].text.strip(),
                'assists_per_game': cols[23].text.strip(),
                'steals_per_game': cols[24].text.strip(),
                'blocks_per_game': cols[25].text.strip(),
                'turnovers_per_game': cols[26].text.strip(),
                'personal_fouls_per_game': cols[27].text.strip(),
                'points_per_game': cols[28].text.strip(),
                'awards': cols[29].text.strip()
            }
            with lock:
                all_per_game_data.append(player_data)
    else:
        print(f'No Per Game table found for {team} {year}')

    # Scrape Per Game postseason Stats
    per_game_table_post = soup.find('table', id='per_game_stats_post')
    if per_game_table_post:
        rows = per_game_table_post.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            if not row.find('td', {'data-stat': 'name_display'}):
                continue
            cols = row.find_all(['th', 'td'])
            player_data = {
                'team': team,
                'year': year,
                'name': cols[1].text.strip(),
                'position_post': cols[3].text.strip(),
                'games_post': cols[4].text.strip(),
                'games_started_post': cols[5].text.strip(),
                'minutes_played_per_game_post': cols[6].text.strip(),
                'field_goals_per_game_post': cols[7].text.strip(),
                'field_goal_attempts_per_game_post': cols[8].text.strip(),
                'field_goal_percentage_post': cols[9].text.strip(),
                'three_point_field_goals_per_game_post': cols[10].text.strip(),
                'three_point_field_goal_attempts_per_game_post': cols[11].text.strip(),
                'three_point_field_goal_percentage_post': cols[12].text.strip(),
                'two_point_field_goals_per_game_post': cols[13].text.strip(),
                'two_point_field_goal_attempts_per_game_post': cols[14].text.strip(),
                'two_point_field_goal_percentage_post': cols[15].text.strip(),
                'effective_field_goal_percentage_post': cols[16].text.strip(),
                'free_throws_per_game_post': cols[17].text.strip(),
                'free_throw_attempts_per_game_post': cols[18].text.strip(),
                'free_throw_percentage_post': cols[19].text.strip(),
                'offensive_rebounds_per_game_post': cols[20].text.strip(),
                'defensive_rebounds_per_game_post': cols[21].text.strip(),
                'total_rebounds_per_game_post': cols[22].text.strip(),
                'assists_per_game_post': cols[23].text.strip(),
                'steals_per_game_post': cols[24].text.strip(),
                'blocks_per_game_post': cols[25].text.strip(),
                'turnovers_per_game_post': cols[26].text.strip(),
                'personal_fouls_per_game_post': cols[27].text.strip(),
                'points_per_game_post': cols[28].text.strip(),
                'awards_post': cols[29].text.strip()
            }
            with lock:
                all_per_game_data_post.append(player_data)
    else:
        print(f'No Per Game_post table found for {team} {year}')

    # Scrape Play-by-Play Stats
    pbp_table = soup.find('table', id='pbp_stats')
    if pbp_table:
        rows = pbp_table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            if not row.find('td', {'data-stat': 'name_display'}):
                continue
            cols = row.find_all(['th', 'td'])
            pbp_data = {
                'team': team,
                'year': year,
                'name': cols[1].text.strip(),
                'pg%': cols[7].text.strip(),
                'sg%': cols[8].text.strip(),
                'sf%': cols[9].text.strip(),
                'pf%': cols[10].text.strip(),
                'c%': cols[11].text.strip(),
                'on_court_+/-': cols[12].text.strip(),
                'on-off_+/-': cols[13].text.strip(),
                'bad_pass_TO': cols[14].text.strip(),
                'lost_ball_TO': cols[15].text.strip(),
                'shooting_fouls': cols[16].text.strip(),
                'offensive_fouls': cols[17].text.strip(),
                'shooting_fouls_drawn': cols[18].text.strip(),
                'offensive_fouls_drawn': cols[19].text.strip(),
                'points generated by assists': cols[20].text.strip(),
                'and1s': cols[21].text.strip()
            }
            with lock:
                all_pbp_data.append(pbp_data)
    else:
        print(f'No PBP table found for {team} {year}')

    # Scrape per game postseason PBP data
    pbp_table_post = soup.find('table', id='pbp_stats_post')
    if pbp_table_post:
        rows = pbp_table_post.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            if not row.find('td', {'data-stat': 'name_display'}):
                continue
            cols = row.find_all(['th', 'td'])
            pbp_data = {
                'team': team,
                'year': year,
                'name': cols[1].text.strip(),
                'pg%_post': cols[7].text.strip(),
                'sg%_post': cols[8].text.strip(),
                'sf%_post': cols[9].text.strip(),
                'pf%_post': cols[10].text.strip(),
                'c%_post': cols[11].text.strip(),
                'on_court_+/-_post': cols[12].text.strip(),
                'on-off_+/-_post': cols[13].text.strip(),
                'bad_pass_to_post': cols[14].text.strip(),
                'lost_ball_to_post': cols[15].text.strip(),
                'shooting_fouls_post': cols[16].text.strip(),
                'offensive_fouls_post': cols[17].text.strip(),
                'shooting_fouls_drawn_post': cols[18].text.strip(),
                'offensive_fouls_drawn_post': cols[19].text.strip(),
                'points_generated_by_assists_post': cols[20].text.strip(),
                'and1s_post': cols[21].text.strip()
            }
            with lock:
                all_pbp_data_post.append(pbp_data)
    else:
        print(f'No PBP_post table found for {team} {year}')

    # Quit the WebDriver
    driver.quit()

def merge_dataframes(all_per_game_data, all_per_game_data_post, all_pbp_data, all_pbp_data_post):
    # Convert lists of dictionaries to DataFrames
    df_per_game = pd.DataFrame(all_per_game_data)
    df_pbp = pd.DataFrame(all_pbp_data)
    df_per_game_post = pd.DataFrame(all_per_game_data_post)
    df_pbp_post = pd.DataFrame(all_pbp_data_post)

    # Merge DataFrames on Player Name and Year
    if not df_per_game.empty and not df_per_game_post.empty and not df_pbp.empty and not df_pbp_post.empty:
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
        print('Data scraping complete and saved to nba_combined_stats.csv')
        return df_combined
    else:
        print('No data to merge. Check if tables were scraped correctly.')
        return None

def main():
    all_per_game_data = []
    all_per_game_data_post = []
    all_pbp_data = []
    all_pbp_data_post = []
    
    # Teams and years to scrape
    nba_teams = ['ATL', 'BRK']  # Add more teams as needed
    years = range(2023, 2025)

    # Use ThreadPoolExecutor to scrape data concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scrape_team_year, team, year, all_per_game_data, all_per_game_data_post, all_pbp_data, all_pbp_data_post) 
                   for team in nba_teams for year in years]
        concurrent.futures.wait(futures)

    # Merge and save data after all threads are done
    merge_dataframes(all_per_game_data, all_per_game_data_post, all_pbp_data, all_pbp_data_post)

if __name__ == '__main__':
    main()