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

<h2 align="center">Results and Recommendations</h2>

<h2 align="center">Reproducing the Results</h2>
