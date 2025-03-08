from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import csv

# Set up Firefox options (run headless to avoid the browser window)
options = Options()
options.headless = True  # Make sure Firefox is in headless mode (no GUI)
options.set_preference("dom.headless", True)  # Set headless mode explicitly

# Initialize the Firefox WebDriver
driver = webdriver.Firefox(options=options)

# List of players to scrape (add more players as needed)
players = [
    "Stephen Curry",
    "LeBron James",
    "Giannis Antetokounmpo",
    "Kevin Durant"
]

# Function to format player name to URL-friendly slug
def format_player_name(name):
    return name.lower().replace(" ", "-")

# Function to scrape ratings for each player
def scrape_2k_ratings(player):
    url = f"https://www.2kratings.com/{format_player_name(player)}"
    print(f"Scraping {player}...")  # Print the player being scraped
    
    # Navigate to the player's page
    driver.get(url)

    # Wait for the page to load completely
    time.sleep(2)

    # Get the page source after it has fully loaded
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the rating table
    table = soup.find("table", class_="table-dark")
    
    if not table:
        print(f"No ratings found for {player}")
        return []

    ratings = []
    # Iterate through each row in the table and extract the data
    for row in table.find_all("tr")[1:]:  # Skip the header row
        cols = row.find_all("td")
        if len(cols) >= 3:
            year = cols[0].text.strip()  # Game year (e.g., NBA 2K25)
            rating = cols[1].text.strip()  # Rating (e.g., 85)
            team = cols[2].text.strip()  # Team name (e.g., Phoenix Suns)

            # Append the data to the ratings list
            ratings.append([player, year, rating, team])
    
    return ratings

# Function to save data to a CSV file
def save_to_csv(data, filename="2k_ratings.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Player", "Year", "Rating", "Team"])
        writer.writerows(data)
    print(f"Data saved to {filename}")

# Main function to scrape ratings for all players
def main():
    all_ratings = []

    for player in players:
        all_ratings.extend(scrape_2k_ratings(player))
        time.sleep(3)  # Delay to avoid detection

    if all_ratings:
        save_to_csv(all_ratings)

    # Close the browser after scraping
    driver.quit()

if __name__ == "__main__":
    main()
