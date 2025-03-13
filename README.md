<h1 align="center">2K Rating Predictor</h1>
<h2 align="center">By Orlando Di Leo, Luke McDonald, Danny Urrutia, Jisoo Yoo</h2>
<p align="center"> <img src="https://scontent.fftw1-1.fna.fbcdn.net/v/t39.30808-6/457287887_954447930032992_7027198657506811338_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=833d8c&_nc_ohc=iGjKj9fD2bEQ7kNvgHdU4ti&_nc_oc=AdgX6ZLx58auaGCYoiCUDVQpHg_fMB_-ID64nehQ2YFJ4vKhMgVefR0XMp0tBZGmhJw&_nc_zt=23&_nc_ht=scontent.fftw1-1.fna&_nc_gid=A2D7yiSXBtrLImay5kh1LTs&oh=00_AYHF6j5SnH6xS7o7JCd-skFoXeLf-k28M-z5VoMcukOC0Q&oe=67D6737B" alt="Description" width="500"> </p>
<h2 align="center">Project Description</h2>
Our goal is to build a model that will accurately predict an NBA player's <b>2K rating</b>, for the video game series <b>NBA 2K</b>, based on their performance the previous season.  Players in the game are typically given an "overall" rating on a <b>1-99 scale</b> that determines their in-game performance.  We are also aiming to identify the statistics that are the most "important" or "relevant" to their rating.

<h2 align="center">The Data</h2>
<h3 align="left">Sources</h3>
- Our real-life NBA season statistics are taken from <a href="https://www.basketball-reference.com">basketball-reference.com</a>. One of the most comprehensive and widely used databases for historical and current basketball (and other sports) data. It provides a vast range of statistics, including advanced metrics, which makes it ideal for predictive modeling. It is cited by many reputable industry sources, such as ESPN. <br>
- Our 2K rating statistics are start-of-season ratings (since the 2K games update their overalls throughout their 1-year live service period) taken from <a href="https://hoopshype.com/nba2k/2024-2025/">HoopsHype</a>, a subsidiary of USA Today Sports. The 2k ratings were corss referenced against a community trusted and run nba 2k ratings site, <a href="2kratings.com"</a>. This also allowed us to confirm that the 2k ratings from Hoops Hype were snapshots of the players' ratings upon game launch

<h3 align="left">Features</h3>
- <b>Age</b>: The player's age at the end of the season. <br>
- <b>Games Played</b>: The number of games during the season where the player played >0 minutes<br>
- <b>Position</b>: A categorical variable indicating the players position: {PG, SG, SF, PF, C}<br>
- <b>Minutes Per Game</b>: The number of minutes the player had per game played<br>
- <b>Points Per Game</b>: The number of points the player scored per game<br>
- <b>Field Goal Percentage</b>: The total percentage of shots made over shots attempted<br>
- <b>3-Point Attempts Per Game</b>: The number of 3-pointers the player attempted per game played<br>
- <b>3-Point Percentage</b>: The total percentage of 3-pointers made over 3-pointers attempted<br>
- <b>Rebounds Per Game</b>: The number of rebounds, offensive and defensive, the player made per game<br>
- <b>Assists Per Game</b>: The number of scoring assists the player made per game<br>
- <b>Steals Per Game</b>: The number of steals the player made per game<br>
- <b>Blocks Per Game</b>: The number of blocks the player made per game<br>
- <b>Turnovers Per Game</b>: The number of turnovers<br>
- <b>Awards</b>: Three dummy variables signifying if the player was an All Star, MVP, or Defensive Player of the Year


<h3 align="left">Collection Methodology</h3>
We originally planned to scrape player ratings from <a href="https://2kratings.com">2KRatings.com</a>, which provides historical 2K ratings. However, the website lacked sufficient data for many players for seasons in the past, leaving our data with significant missing 2k ratings. Instead, we pivoted to <a href="https://hoopshype.com/nba2k/2024-2025/">HoopsHype.com</a>, Which had more complete data and consistently structured urls, giving us a more complete dataset.

For real-world NBA statistics, we scraped Basketball-Reference using Python’s <b>BeautifulSoup</b> and <b>Selenium</b> libraries. Selenium was used for Basketball-Reference, as we encountered issues retrieving data directly with BeautifulSoup. We iterated through team pages for each season, extracting player performance metrics. Our scraper collected per-game statistics and awards information and some play-by-play statistics.

After scraping, we joined the datasets on player name and year, formatting to ensure consistency across sources by stripping excess whitespace, punctuation, and converting them to unicode-normalized formats to handle special characters and accents. This helped align names as much as possible between Basketball-Reference and HoopsHype, but inevitably, some players still lacked a matched 2K rating after the join. This occurred for two main reasons:

<ol>
  <li>Free Agents – Some players appeared in Basketball-Reference's stats but were not assigned a 2K rating at the start of the season because they were unsigned free agents.</li>
  <li>Name Mismatches – Even after standardization, some names did not match exactly between the two sources due to differences in formatting, abbreviations, or middle name usage.</li>
</ol>

Unmatched players were dropeed from the dataset. After joining the datasets, we conducted spot checks to verify the accuracy of the merged data against the original sources.

<h3 align="left">Limitations</h3>
We decided to omit playoff statistics, since most players had empty data cells for playoff statistics in any given season. Presumably, this could affect our model since high playoff-performers are seen in high regard by both the public and the game developers.

While we made efforts to manually check and resolve inconsistencies in player names, the data is missing unmatched players which were dropeed from the dataset.

<br>

<h2 align="center">The Model(s)</h2>

### KNN:
**K-Nearest Neighbors** predicts player ratings by calculating distances between players based on their performance metrics. This estimates ratings relative to other similar players’ statistics and features. This is effective since the ratings consistently range between 40-99, so the model will work when applied to unseen and future data. However, with so many performance metrics, distances between players become less meaningful, and the model struggles to identify which features are most important for predicting 2K ratings. As a result, less relevant features can hurt the model’s accuracy, limiting its overall performance.

**Train Metrics:**  
- Training MSE: 9.613644652967167  
- Training MAE: 2.17810248928604  
- Training R²: 0.824003325873335

**Test Metrics:**  
- Testing MSE: 11.141943702230783  
- Testing MAE: 2.3165413533834585  
- Testing R²: 0.7958398467520803  
- Total observations: 5318 

### OLS

**The Ordinary Least Squares model** uses all the features from the feature list. It is common in many sports for a player to reach a peak age where their performance is at its best. Therefore, we included an age squared variable to control for the non-linear effects of a player's age on their performance and resulting rating. All other features are assumed to have a linear effect on rating, which is a limitation of the simple OLS model. 

**Train Metrics:**  
- Training MSE: 10.728237088033223  
- Training MAE: 2.281645166361385  
- Training R²: 0.8035985190951043  

**Test Metrics:**  
- Testing MSE: 10.356485222296063  
- Testing MAE: 2.2197833920093824  
- Testing R²: 0.8102322479272221  
- Total observations: 5318

<h2 align="center">Reproducing the Results</h2>

**The required Python packages are:**  

- **pandas** – for data manipulation and analysis  
- **requests** – for making HTTP requests to fetch web pages  
- **beautifulsoup** – for parsing HTML and extracting data from web pages  
- **selenium** – for web scraping basketball-reference.com  
- **scikit-learn** – for machine learning models and data preprocessing  

These can be installed using pip (or pip3):  

```bash
pip install pandas requests beautifulsoup4 selenium scikit-learn
```

## Data Scraping:  

After downloading and opening the repo, make the working directory **"data_scraping"** within the main project folder:  

```bash
cd data_scraping
```

Run the Python file **scrape_clean.py**. This file will scrape the 2010-2024 NBA stats (the teams and years can be adjusted) from basketball-reference.com, 2K stats from hoopshype.com from NBA 2K11 to NBA 2K25, and then merge and clean the data, dropping observations with missing data where joins did not find matching records. This will output four .csv files:  

- **nba_stats.csv** - all of the scraped NBA data for the specified teams and years  
- **nba2k_ratings.csv** - all of the scraped 2K ratings for the specified years  
- **nba_combined_stats.csv** - uncleaned merged datasets  
- **nba_2k_cleaned_final.csv** - the final merged dataset, formatted for analysis with missing records dropped  


*(The scraping script uses geckodriver, this file is already in the data_scraping file)*

*(If you do not want to run this script, the data is also stored in the folder **data_v2**.)*

### Running the Models

From the top level of the repository, run the following code:
```bash
python3 models/[model name].py
```
according to the file names. The test and train metrics will be printed, along with coefficients and feature importances as appropriate.
