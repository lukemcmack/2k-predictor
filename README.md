<h1 align="center">2K Rating Predictor</h1>
<h2 align="center">By Orlando Di Leo, Luke McDonald, Danny Urrutia, Jisoo Yoo</h2>
<p align="center"> <img src="https://scontent.fftw1-1.fna.fbcdn.net/v/t39.30808-6/457287887_954447930032992_7027198657506811338_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=833d8c&_nc_ohc=iGjKj9fD2bEQ7kNvgHdU4ti&_nc_oc=AdgX6ZLx58auaGCYoiCUDVQpHg_fMB_-ID64nehQ2YFJ4vKhMgVefR0XMp0tBZGmhJw&_nc_zt=23&_nc_ht=scontent.fftw1-1.fna&_nc_gid=A2D7yiSXBtrLImay5kh1LTs&oh=00_AYHF6j5SnH6xS7o7JCd-skFoXeLf-k28M-z5VoMcukOC0Q&oe=67D6737B" alt="Description" width="500"> </p>
<h2 align="center">Project Description</h2>
Our goal is to build a model that will accurately predict an NBA player's <b>2K rating</b>, for the video game series <b>NBA 2K</b>, based on their performance the previous season.  Players in the game are typically given an "overall" rating on a <b>1-99 scale</b> that determines their in-game performance.  We are also aiming to identify the statistics that are the most "important" or "relevant" to their rating.

<h2 align="center">The Data</h2>
<h3 align="left">Sources</h3>
- Our real-life NBA season statistics are taken from <a href="https://www.basketball-reference.com">basketball-reference.com</a>. <br>
- Our 2K rating statistics are start-of-season ratings (since the 2K games update their overalls throughout their 1-year live service period) taken from <a href="https://hoopshype.com/nba2k/2024-2025/">HoopsHype</a>, a subsidiary of USA Today Sports.

<h3 align="left">Features</h3>
- <b>Age</b>: The player's age at the end of the season.
- <b>Games Played</b>: The number of games during the season where the player played >0 minutes
- <b>Position</b>: A categorical variable indicating the players position: {PG, SG, SF, PF, C}
- <b>Minutes Per Game</b>: The number of minutes the player had per game played
- <b>Points Per Game</b>: The number of points the player scored per game
- <b>Field Goal Percentage</b>: The total percentage of shots made over shots attempted
- <b>3-Point Attempts Per Game</b>: The number of 3-pointers the player attempted per game played
- <b>3-Point Percentage</b>: The total percentage of 3-pointers made over 3-pointers attempted
- <b>Rebounds Per Game</b>: The number of rebounds, offensive and defensive, the player made per game
- <b>Assists Per Game</b>: The number of scoring assists the player made per game
- <b>Steals Per Game</b>: The number of steals the player made per game
- <b>Blocks Per Game</b>: The number of blocks the player made per game
- <b>Turnovers Per Game</b>: The number of turnovers 


<h3 align="left">Collection Methodology</h3>
<b> LUKE WRITE THIS UP!!! </b>

<h3 align="left">Limitations</h3>
We decided to omit playoff statistics, since most players had empty data cells for playoff statistics in any given season. Presumably, this could affect our model since high playoff-performers are seen in high regard by both the public and the game developers.<br>

<h2 align="center">The Model(s)</h2>

<h2 align="center">Results and Recommendations</h2>

<h2 align="center">Reproducing the Results</h2>