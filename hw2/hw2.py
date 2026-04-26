import pandas as pd

# Load the CSV directly from your local file
anime_data = pd.read_csv('anime.csv')

# Clean the data
anime_data_extracted = anime_data[anime_data['Score'] != 'Unknown'].copy()
anime_data_extracted['Score'] = pd.to_numeric(anime_data_extracted['Score'])

# Homework function
def homework(anime_data_extracted):
    return anime_data_extracted.groupby('Type')['Score'].mean().sort_values(ascending=False)

# Run and print the result
result = homework(anime_data_extracted)
print(result)