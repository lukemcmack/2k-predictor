from nba_stat_scraper import write_nba_csv
from hoopshype_scraper import save_2k_ratings_to_csv
from clean_data import clean_data
import pandas as pd
import threading

lock = threading.Lock()
player_data_dict = {}


def main():
    nba_teams = [
        "ATL",
        "BRK",
        "BOS",
        "NJN",
        "CHA",
        "CHI",
        "CHO",
        "CLE",
        "DET",
        "IND",
        "MIA",
        "MIL",
        "NYK",
        "ORL",
        "PHI",
        "TOR",
        "WAS",
        "DAL",
        "DEN",
        "GSW",
        "HOU",
        "LAC",
        "LAL",
        "MEM",
        "MIN",
        "NOP",
        "NOH",
        "OKC",
        "PHO",
        "POR",
        "SAC",
        "SAS",
        "UTA",
    ]
    years = range(2010, 2025)

    write_nba_csv(nba_teams, years, file_path="nba_stats.csv")
    save_2k_ratings_to_csv(min(years), max(years), filename="nba2k_ratings.csv")

    df_2k = pd.read_csv("nba2k_ratings.csv")
    df_nba = pd.read_csv("nba_stats.csv")

    df_merged = pd.merge(
        df_nba,
        df_2k,
        on=[
            ("name".encode("ascii", "ignore").decode("utf-8"))
            .lower()
            .replace(" ", "-")
            .replace(".", "")
            .replace("'", ""),
            "year",
        ],
        how="left",
    )
    if not df_merged.empty:
        print("NBA stats and 2K ratings successfully merged.")
    else:
        print(
            "Merge failed. Check if both CSVs contain matching player names and years."
        )

    if not df_merged.empty:
        df_merged.to_csv("nba_combined_stats.csv", index=False)
        print("Final combined data saved to nba_combined_stats.csv")
    else:
        print("No data to save. Check if merge was successful.")

    clean_data(
        input_file_name="nba_combined_stats.csv",
        output_file_name="nba_2k_cleaned_final.csv",
    )


if __name__ == "__main__":
    main()
