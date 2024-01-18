import os
import csv
import time
import logging
import aiohttp
import asyncio

# Configure logging
logging.basicConfig(filename='error_log_lgbt.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Google Perspective API endpoint
api_endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

# Google Perspective API key
api_key = "AIzaSyBOXtUn3gzBlz_s9HeZJZPIC9Kg8sLgJZw"  # Replace with your actual API key

async def analyze_comment(session, comment_text):
    params = {"key": api_key}
    data = {
        "comment": {"text": comment_text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "THREAT": {},
            "IDENTITY_ATTACK": {},
        },
    }

    async with session.post(api_endpoint, params=params, json=data) as response:
        result = await response.json()

        # Check if 'attributeScores' is present in the result
        if 'attributeScores' in result:
            return result['attributeScores']
        else:
            # Log a warning when 'attributeScores' is missing
            logging.warning("Missing 'attributeScores' in API response.")
            return None

async def process_comments_async(session, input_csv_path, output_csv_path):
    comments_data = []
    with open(input_csv_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            comments_data.append(row)

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as output_csv:
        # Update the fieldnames list to include all columns from the input CSV file
        fieldnames = ['id', 'subreddit', 'body', 'author', 'created_utc', 'toxic', 'severe_toxic', 'threat', 'identity_attack']
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()

        tasks = []
        for i, comment_data in enumerate(comments_data, start=1):
            task = process_comment_async(session, i, comment_data, writer)
            tasks.append(task)

        await asyncio.gather(*tasks)

    print(f'Labels successfully written to {output_csv_path}')

async def process_comment_async(session, i, comment_data, writer):
    scores = await analyze_comment(session, comment_data['body'])

    while scores is None:
        print(f"Error: Retrying for comment {i}")
        # Handle the case when scores are not available
        comment_data.update({
            'toxic': None,
            'severe_toxic': None,
            'threat': None,
            'identity_attack': None,
        })
        scores = await analyze_comment(session, comment_data['body'])

    comment_data.update({
        'toxic': 1 if scores.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0) >= 0.5 else 0,
        'severe_toxic': 1 if scores.get("SEVERE_TOXICITY", {}).get("summaryScore", {}).get("value", 0) >= 0.5 else 0,
        'threat': 1 if scores.get("THREAT", {}).get("summaryScore", {}).get("value", 0) >= 0.5 else 0,
        'identity_attack': 1 if scores.get("IDENTITY_ATTACK", {}).get("summaryScore", {}).get("value", 0) >= 0.5 else 0,
    })

    print(f"No error {i}")

    writer.writerow(comment_data)

# Specify the directory containing the input CSV files
input_csv_directory = 'test_dir'  # Replace with your actual directory path

async def main():
    async with aiohttp.ClientSession() as session:
        # Iterate over each input CSV file in the directory
        for input_csv_file in os.listdir(input_csv_directory):
            if input_csv_file.endswith('.csv'):
                input_csv_path = os.path.join(input_csv_directory, input_csv_file)

                # Create a corresponding output CSV file for each input file
                output_csv_file = f"{os.path.splitext(input_csv_file)[0]}_output.csv"
                output_csv_path = os.path.join('test_output_subreddit', output_csv_file)

                # Process comments from the input CSV file and create an output CSV file
                await process_comments_async(session, input_csv_path, output_csv_path)

# Run the asynchronous event loop
if __name__ == "__main__":
    asyncio.run(main())
