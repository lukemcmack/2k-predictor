import requests
from bs4 import BeautifulSoup
import csv

def scrape_nba2k_ratings(year):
    # Construct the URL
    url = f"https://hoopshype.com/nba2k/{year}-{year+1}/"
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data for {year}-{year+1}")
        return []
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table containing the ratings
    table = soup.find('table', class_='hh-salaries-ranking-table')
    
    # Check if the table was found
    if not table:
        print(f"Table not found for {year}-{year+1}")
        return []
    
    # Extract the rows from the table body
    rows = table.find('tbody').find_all('tr')
    
    # Iterate over the rows and extract player names and ratings
    ratings = []
    for row in rows:
        rank = row.find('td', class_='rank').text.strip()
        name = row.find('td', class_='name').text.strip()
        rating = row.find('td', class_='value').text.strip()
        ratings.append((year, rank, name, rating))
    
    return ratings

def save_2k_ratings_to_csv(start_year, end_year, filename="nba2k_ratings.csv"):
    # Open the CSV file for writing
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["year", "rank", "name", "rating"])
        
        # Loop through the range of years
        for year in range(start_year, end_year + 1):
            print(f"Scraping data for {year}-{year+1}...")
            ratings = scrape_nba2k_ratings(year)
            if ratings:
                # Write the ratings for the current year to the CSV
                writer.writerows(ratings)
                print(f"Data for {year}-{year+1} saved to {filename}")
            else:
                print(f"No data found for {year}-{year+1}")


def main():
    start_year = 2010
    end_year = 2024
    save_2k_ratings_to_csv(start_year, end_year)

if __name__ == '__main__':
    main()