import pandas as pd

def clean_data(input_file_name = 'nba_combined_stats.csv', output_file_name = 'nba_2k_cleaned_final.csv'):
    df = pd.read_csv(input_file_name)
    df['experience'] = df['experience'].replace('R', '0')
   
   #Coding dummy variables for awards.
    df['AS'] = df['awards'].apply(lambda x: 1 if pd.notna(x) and 'AS' in x else 0)
    df['MVP'] = df['awards'].apply(lambda x: 1 if pd.notna(x) and 'MVP-1' in x else 0)
    df['DPOY'] = df['awards'].apply(lambda x: 1 if pd.notna(x) and 'DPOY-1' in x else 0)
    
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