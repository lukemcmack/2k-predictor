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
import os
import logging

lock = threading.Lock()

# Dictionary to store all player data
player_data_dict = {}

def scrape_team_year(team, year):
    global player_data_dict

    options = Options()
    options.add_argument('--headless')  # Run Firefox in headless mode
    service = Service('geckodriver')
    driver = webdriver.Firefox(service=service, options=options)

    url = f'https://www.basketball-reference.com/teams/{team}/{year}.html'
    print(f'Accessing URL: {url}')
    driver.get(url)

    # Wait for the page to load completely
    try:
        WebDriverWait(driver, .5).until(
            EC.presence_of_element_located((By.ID, 'per_game_stats')))
    except Exception as e:
        print(f'Failed to load page for {team} {year}: {e}')
        driver.quit()
        return {
            'team': team,
            'year': year,
            'wins': None,
            'losses': None
        }

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Helper function to update player data
    def update_player_data(player_key, new_data):
        with lock:
            if player_key in player_data_dict:
                player_data_dict[player_key].update(new_data)
            else:
                player_data_dict[player_key] = new_data

    # Scrape Per Game Stats
    per_game_table = soup.find('table', id='per_game_stats')
    if per_game_table:
        rows = per_game_table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            if not row.find('td', {'data-stat': 'name_display'}):
                continue
            cols = row.find_all(['th', 'td'])
            player_key = (team, year, cols[1].text.strip())
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
            update_player_data(player_key, player_data)
    else:
        print(f'No Per Game table found for {team} {year}')

    # Scrape Play-by-Play Stats
    pbp_table = soup.find('table', id='pbp_stats')
    if pbp_table:
        rows = pbp_table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            if not row.find('td', {'data-stat': 'name_display'}):
                continue
            cols = row.find_all(['th', 'td'])
            player_key = (team, year, cols[1].text.strip())
            pbp_data = {
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
                'points_generated_by_assists': cols[20].text.strip(),
                'and1s': cols[21].text.strip()
            }
            update_player_data(player_key, pbp_data)
    else:
        print(f'No PBP table found for {team} {year}')

    # Scrape Height (in inches) and Experience from Roster Table
    roster_table = soup.find('table', id='roster')
    if roster_table:
        rows = roster_table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all(['th', 'td'])
            player_name = cols[1].text.strip()
            height_ft_in = cols[3].text.strip()  # Height in feet-inches (e.g., "6-11")
            exp = cols[7].text.strip()  # Experience (e.g., "R" or "11")

            # Convert height from feet-inches to inches
            height_inches = None
            if '-' in height_ft_in:
                try:
                    feet, inches = height_ft_in.split('-')
                    height_inches = int(feet) * 12 + int(inches)
                except ValueError:
                    print(f"Invalid height format for {player_name}: {height_ft_in}")

            # Update player data with height and experience
            player_key = (team, year, player_name)
            player_data = {
                'height_inches': height_inches,
                'experience': exp
            }
            update_player_data(player_key, player_data)

    # Scrape Team Record
    record_tag = soup.find('strong', string="Record:")
    if record_tag:
        # Navigate to the parent <p> tag and get its text
        record_text = record_tag.find_parent('p').get_text(strip=True).replace('Record:', '').strip()
        # Extract wins and losses from the record (e.g., "47-35, Finished 8th in NBA Western Conference")
        wins_losses = record_text.split(',')[0].strip()  # Get "47-35"
        if '-' in wins_losses:
            wins, losses = wins_losses.split('-')
            team_record = {
                'team': team,
                'year': year,
                'wins': wins.strip(),
                'losses': losses.strip()
            }
        else:
            print(f"No valid wins-losses format found for {team} {year}.")
            team_record = {
                'team': team,
                'year': year,
                'wins': None,
                'losses': None
            }
    else:
        print(f"Record tag not found for {team} {year}.")
        team_record = {
            'team': team,
            'year': year,
            'wins': None,
            'losses': None
        }

    # Quit the WebDriver
    driver.quit()

    return team_record  # Return the team record for later use

def write_nba_csv(nba_teams, years, file_path='nba_stats.csv'):
    global player_data_dict

    # Use ThreadPoolExecutor to scrape data concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()-1) as executor:
        futures = [executor.submit(scrape_team_year, team, year) 
                   for team in nba_teams for year in years]
        team_records = [future.result() for future in concurrent.futures.as_completed(futures)]

    # Filter out None values from team_records
    team_records = [record for record in team_records if record is not None]

    # Convert player_data_dict to DataFrame
    if not player_data_dict:
        print("No player data scraped. Exiting.")
        return
    all_data = pd.DataFrame(list(player_data_dict.values()))

    # Convert team_records to DataFrame
    team_records_df = pd.DataFrame(team_records)

    # Left join all_data with team_records_df on team and year
    if not all_data.empty and not team_records_df.empty:
        all_data = pd.merge(all_data, team_records_df, on=['team', 'year'], how='left')
        print("Team records successfully joined with player data.")
    else:
        print("No data to merge. Check if tables were scraped correctly.")

    # Save the combined DataFrame to CSV
    if not all_data.empty:
        all_data.to_csv(file_path, index=False)
        print(f'Data scraping complete and saved to {file_path}')
    else:
        print('No data scraped. Check if tables were found.')

def main():
    # Teams and years to scrape
    nba_teams = ['ATL', 'BRK']  # Add more teams as needed
    years = range(2023, 2025)
    write_nba_csv(nba_teams, years)

if __name__ == '__main__':
    main()