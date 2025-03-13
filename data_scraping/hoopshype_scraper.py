import requests
from bs4 import BeautifulSoup
import csv

def scrape_nba2k_ratings(year):
    # 2024-2025 will get 2K25 data
    url = f"https://hoopshype.com/nba2k/{year}-{year+1}/"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data for {year}-{year+1}")
        return []

    # Get the ratings table and extract rows
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="hh-salaries-ranking-table")
    if not table:
        print(f"Table not found for {year}-{year+1}")
        return []
    rows = table.find("tbody").find_all("tr")
    
    # Iterate over the rows and extract player names and ratings
    ratings = []
    for row in rows:
        rank = row.find("td", class_="rank").text.strip()
        name = row.find("td", class_="name").text.strip()
        rating = row.find("td", class_="value").text.strip()
        ratings.append((year, rank, name, rating))
    
    return ratings

def save_2k_ratings_to_csv(start_year, end_year, filename="nba2k_ratings.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["year", "rank", "name", "rating"])
        for year in range(start_year, end_year + 1):
            print(f"Scraping data for {year}-{year+1}...")
            ratings = scrape_nba2k_ratings(year)
            if ratings:
                # Write the ratings for the current year to the CSV
                writer.writerows(ratings)
                print(f"Data for {year}-{year+1} saved to {filename}")
            else:
                print(f"No data found for {year}-{year+1}")

# set years here that you'd like to scrape
def main():
    start_year = 2010
    end_year = 2024
    save_2k_ratings_to_csv(start_year, end_year)

if __name__ == "__main__":
    main()