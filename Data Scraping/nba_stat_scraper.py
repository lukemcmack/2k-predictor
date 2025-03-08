import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

teams = ["CLE", "DET", "BOS"]
years = range(2000, 2006)

# List to store player data
player_data = []

# Function to scrape the data from each page
def scrape_team_data(team, year):
    url = f"https://www.basketball-reference.com/teams/{team}/{year}.html"
    
    # Print the URL being tried
    print(f"Trying URL: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(f"Connection successful for {team} in {year}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table with the specified class and ID
        table = soup.find('table', {'class': 'stats_table sortable soc now_sortable', 'id': 'per_game_stats'})

        if table:
            headers = []
            for th in table.find_all('th'):
                headers.append(th.get_text(strip=True))

            rows = table.find_all('tr')[1:]

            data = []

            for row in rows:
                row_data = []
                columns = row.find_all('td')
                
                if columns:
                    for col in columns:
                        row_data.append(col.get_text(strip=True))
                    data.append(row_data)
            
            df = pd.DataFrame(data, columns=headers)
            
            df.to_csv(f'nba_{team}_{year}_per_game_stats.csv', index=False)
            print(f"Data saved for {team} in {year}")
            
            return df
        else:
            print(f"Table not found for {team} in {year}")
            return []
    else:
        print(f"Failed to connect for {team} in {year}. Status code: {response.status_code}")
        return []

for team in teams:
    for year in years:
        scrape_team_data(team, year)
