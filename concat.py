import os
import pandas as pd

# Set the directory containing CSV files
directory_path = 'output_subreddit'

# Get a list of all CSV files in the directory
csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

# Check if there are any CSV files in the directory
if not csv_files:
    print("No CSV files found in the directory.")
else:
    # Initialize an empty DataFrame to store the concatenated data
    concatenated_data = pd.DataFrame()

    # Iterate through each CSV file and concatenate the data
    for csv_file in csv_files:
        file_path = os.path.join(directory_path, csv_file)
        current_data = pd.read_csv(file_path)
        concatenated_data = pd.concat([concatenated_data, current_data], ignore_index=True)

    # Save the concatenated data to a new CSV file or perform further processing
    concatenated_data.to_csv('total_comments_labelled.csv', index=False)
    print("Concatenation complete. Data saved to concatenated_data.csv.")
