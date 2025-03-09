from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import csv
import concurrent.futures
import time

# Read the player names from your CSV file (assuming there's a column 'name' that contains player names)
df = pd.read_csv('nba_combined_stats.csv')

# Assuming the player names are in a column called 'name' (adjust if necessary)
player_names = df['name'].drop_duplicates()

# Function to convert player name to slug format ('firstname-lastname')
def format_player_name(name):
    return name.lower().replace(" ", "-")

player_slugs = player_names.apply(format_player_name).tolist()

# Function to scrape ratings for each player
def scrape_2k_ratings(player):
    options = Options()
    options.add_argument('--headless')  # Run Firefox in headless mode
    service = Service('geckodriver')
    driver = webdriver.Firefox(service=service, options=options)
    
    url = f"https://www.2kratings.com/{player}"
    print(f"Scraping {player}...")

    # Navigate to specific player's page
    driver.get(url)
    time.sleep(2)  # Wait for the page to load
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", class_="table-dark")
    
    if not table:
        print(f"No ratings found for {player}")
        driver.quit()
        return []

    ratings = []
    # Iterate through each row in the table and extract the data
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) >= 3:
            year = cols[0].text.strip()
            rating = cols[1].text.strip()
            team = cols[2].text.strip()

            # Append the data to the ratings list
            ratings.append([player, year, rating, team])
    driver.quit()
    
    return ratings

# Function to save data to a CSV file
def save_to_csv(data, filename="2k_ratings.csv"):
    # Check if file exists to decide whether to write header or not
    file_exists = False
    try:
        with open(filename, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    # Open the file and write data
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Player", "Year", "Rating", "Team"])  # Write header if file is new
        writer.writerows(data)
    print(f"Data saved to {filename}")

# Function to handle scraping for multiple players in parallel
def scrape_ratings_for_players(players):
    all_ratings = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scrape_2k_ratings, player) for player in players]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                all_ratings.extend(result)

    if all_ratings:
        save_to_csv(all_ratings)

# Main function to start scraping ratings for all players
def main():
    scrape_ratings_for_players(player_slugs)

if __name__ == "__main__":
    main()
