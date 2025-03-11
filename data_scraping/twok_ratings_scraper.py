from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import csv
import concurrent.futures
import time
import unicodedata
import threading

# Global lock for thread-safe file writing
lock = threading.Lock()

# Function to convert player name to slug format ('firstname-lastname')
def format_player_name(name):
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
    name = name.lower().replace(" ", "-").replace(".", "").replace("'", "")
    return name

# Helper function to extract height and wingspan from <p> tags
def extract_height_wingspan(soup):
    height = "N/A"
    wingspan = "N/A"
    p_tags = soup.find_all("p", class_="mb-1 my-lg-0")
    for p in p_tags:
        text = p.text.strip()
        if "Height:" in text:
            span = p.find("span")
            if span:
                height = span.text.strip()
        elif "Wingspan:" in text:
            span = p.find("span")
            if span:
                wingspan = span.text.strip()
    return height, wingspan

# Function to scrape ratings, height, and wingspan for each player
def scrape_2k_data(player):
    options = Options()
    options.add_argument('--headless')  # Run Firefox in headless mode
    service = Service('geckodriver')
    driver = webdriver.Firefox(service=service, options=options)
    
    url = f"https://www.2kratings.com/{player}"
    print(f"Scraping {player}...")

    try:
        driver.get(url)
        # Wait for the ratings table to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-dark"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract height and wingspan
        height, wingspan = extract_height_wingspan(soup)

        # Extract ratings data
        table = soup.find("table", class_="table-dark")
        if not table:
            print(f"No ratings found for {player}")
            return []

        ratings = []
        for row in table.find_all("tr")[1:]:  # Skip header row
            cols = row.find_all("td")
            if len(cols) >= 3:
                year = cols[0].text.strip()
                rating = cols[1].text.strip()
                team = cols[2].text.strip()
                ratings.append([player, year, rating, team, height, wingspan])

        return ratings

    except Exception as e:
        print(f"Error scraping {player}: {e}")
        return []
    finally:
        driver.quit()

# Function to save merged data to CSV (thread-safe)
def save_to_csv(data, filename="2k_ratings_wingspan_height.csv"):
    with lock:
        file_exists = False
        try:
            with open(filename, "r"):
                file_exists = True
        except FileNotFoundError:
            pass

        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["name_slug", "twok_year", "Rating", "Team", "Height", "Wingspan"])  # Write header if file is new
            writer.writerows(data)

        print(f"Data saved to {filename}")

# Function to scrape multiple players in parallel
def scrape_players(players):
    all_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:  # Limit concurrent workers
        futures = [executor.submit(scrape_2k_data, player) for player in players]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                all_data.extend(result)
            time.sleep(1)  # Add a delay between requests to avoid overwhelming the server

    if all_data:
        save_to_csv(all_data)

# Main function
def main():
    # Read the player names from CSV
    df = pd.read_csv('nba_combined_stats.csv')
    player_names = df['name'].drop_duplicates()

    player_slugs = player_names.apply(format_player_name).tolist()

    scrape_players(player_slugs)

if __name__ == "__main__":
    main()