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

all_per_game_data = []
all_pbp_data = []
lock = threading.Lock()

def scrape_team_year(team, year):
    options = Options()
    options.add_argument('--headless')  # Run Firefox in headless mode
    service = Service('geckodriver.exe')
    driver = webdriver.Firefox(service=service, options=options)

    url = f'https://www.basketball-reference.com/teams/{team}/{year}.html'
    print(f'Accessing URL: {url}')
    driver.get(url)

    # Wait for the page to load completely
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'per_game_stats'))
        )
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
                'Team': team,
                'Year': year,
                'Name': cols[1].text.strip(),
                'Age': cols[2].text.strip(),
                'Position': cols[3].text.strip(),
                'Games': cols[4].text.strip(),
                'Games Started': cols[5].text.strip(),
                'Minutes Played Per Game': cols[6].text.strip(),
                'Field Goals Per Game': cols[7].text.strip(),
                'Field Goal Attempts Per Game': cols[8].text.strip(),
                'Field Goal Percentage': cols[9].text.strip(),
                '3-Point Field Goals Per Game': cols[10].text.strip(),
                '3-Point Field Goal Attempts Per Game': cols[11].text.strip(),
                '3-Point Field Goal Percentage': cols[12].text.strip(),
                '2-Point Field Goals Per Game': cols[13].text.strip(),
                '2-Point Field Goal Attempts Per Game': cols[14].text.strip(),
                '2-Point Field Goal Percentage': cols[15].text.strip(),
                'Effective Field Goal Percentage': cols[16].text.strip(),
                'Free Throws Per Game': cols[17].text.strip(),
                'Free Throw Attempts Per Game': cols[18].text.strip(),
                'Free Throw Percentage': cols[19].text.strip(),
                'Offensive Rebounds Per Game': cols[20].text.strip(),
                'Defensive Rebounds Per Game': cols[21].text.strip(),
                'Total Rebounds Per Game': cols[22].text.strip(),
                'Assists Per Game': cols[23].text.strip(),
                'Steals Per Game': cols[24].text.strip(),
                'Blocks Per Game': cols[25].text.strip(),
                'Turnovers Per Game': cols[26].text.strip(),
                'Personal Fouls Per Game': cols[27].text.strip(),
                'Points Per Game': cols[28].text.strip(),
                'Awards': cols[29].text.strip()
            }
            with lock:
                all_per_game_data.append(player_data)
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
            pbp_data = {
                'Team': team,
                'Year': year,
                'Name': cols[1].text.strip(),
                'Age': cols[2].text.strip(),
                'Position': cols[3].text.strip(),
                'Games': cols[4].text.strip(),
                'Games Started': cols[5].text.strip(),
                'Minutes Played': cols[6].text.strip(),
                'PG%': cols[7].text.strip(),
                'SG%': cols[8].text.strip(),
                'SF%': cols[9].text.strip(),
                'PF%': cols[10].text.strip(),
                'C%': cols[11].text.strip(),
                'OnCourt +/-': cols[12].text.strip(),
                'On-Off +/-': cols[13].text.strip(),
                'Bad Pass TO': cols[14].text.strip(),
                'Lost Ball TO': cols[15].text.strip(),
                'Shooting Fouls': cols[16].text.strip(),
                'Offensive Fouls': cols[17].text.strip(),
                'Shooting Fouls Drawn': cols[18].text.strip(),
                'Points Generated by Assists': cols[19].text.strip(),
                'And1s': cols[20].text.strip(),
                'Shots Blocked': cols[21].text.strip(),
                'Awards': cols[22].text.strip()
            }
            with lock:
                all_pbp_data.append(pbp_data)
    else:
        print(f'No PBP table found for {team} {year}')

    # Quit the WebDriver
    driver.quit()

# Teams and years to scrape
nba_teams = ['ATL', 'BRK','BOS', 'NJN', 'CHA', 'CHI', 'CHO', 'CLE', 'DET', 'IND', 'MIA', 'MIL', 
             'NYK', 'ORL', 'PHI', 'TOR', 'WAS', 'DAL', 'DEN', 'GSW', 'HOU', 'LAC', 
             'LAL', 'MEM', 'MIN', 'NOP', 'NOH', 'OKC', 'PHO', 'POR', 'SAC', 'SAS', 'UTA']
years = range(2010, 2025)

## (2012-2013 onward) BRK = NJN  = Nets; CHA = (2014-15 onwards)CHO = Bobcats; NOP = NOH = Pelicans

# Use ThreadPoolExecutor to scrape data concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(scrape_team_year, team, year) for team in nba_teams for year in years]
    concurrent.futures.wait(futures)

# Convert lists of dictionaries to DataFrames
df_per_game = pd.DataFrame(all_per_game_data)
df_pbp = pd.DataFrame(all_pbp_data)

# Debugging: Print columns of both DataFrames
print('Per Game Stats Columns:', df_per_game.columns.tolist())
print('PBP Stats Columns:', df_pbp.columns.tolist())

# Merge DataFrames on Player Name and Year
if not df_per_game.empty and not df_pbp.empty:
    df_combined = pd.merge(df_per_game, df_pbp, on=['Team', 'Year', 'Name'], how='left')
        # Update team abbreviations, since abbrevations changed for these teams
    df_combined['Team'] = df_combined['Team'].replace({
        'CHO': 'CHA',
        'NJN': 'BRK'
        'NOP': 'NOH'
    })
    # Export combined DataFrame to CSV
    df_combined.to_csv('nba_combined_stats.csv', index=False)
    print('Data scraping complete and saved to nba_combined_stats.csv')
else:
    print('No data to merge. Check if tables were scraped correctly.')