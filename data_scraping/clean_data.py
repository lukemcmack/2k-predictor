import pandas as pd

def clean_data(input_file_name = 'nba_combined_stats.csv', output_file_name = 'nba_2k_cleaned_final.csv'):
    df = pd.read_csv(input_file_name)
    df['experience'] = df['experience'].replace('R', '0')
    # Define a function to label the 'awards' column
    def label_awards(awards):
        if pd.isna(awards):  # Check if the value is null
            return 0
        elif 'AS' in awards:  # Check if 'AS' is in the awards string
            return 2
        elif awards:  # Check if the awards field is non-empty
            return 1
        else:
            return 0  # Fallback for any unexpected cases
    df = df.drop(df[df['name'] == 'Team Total'].index)

    initial_count = len(df)
    # Convert 'rating' column to numeric, coercing non-numeric values to NaN
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    # Drop rows where 'rating' is NaN
    df_cleaned = df.dropna(subset=['rating'])
    final_count = len(df_cleaned)
    # Calculate the number of dropped records
    dropped_count = initial_count - final_count
    print(f"Number of records dropped due to missing ratings: {dropped_count}")
    df_cleaned.to_csv(output_file_name, index=False)
    print(df_cleaned)

def main():
    clean_data()

if __name__ == '__main__':
    main()