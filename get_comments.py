import praw
import csv
from datetime import datetime
from praw.models import MoreComments

# Reddit API credentials
reddit = praw.Reddit(client_id="gw5cab9dcsXMnRI5MNfTrw",
                     client_secret="P0ixQbX06ow2AQqH6yTRSxMw9KjlfQ",
                     user_agent="praw_scraper_2.0")

def comment_generator(subreddit, num_comments):
    comments = subreddit.comments(limit=num_comments)
    for comment in comments:
        yield comment
    for submission in subreddit.new(limit=num_comments):
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            yield comment

def extract_and_store_comments_csv(subreddit_names, num_comments_per_batch=50, csv_filename="announce_commments.csv"):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['id', 'subreddit', 'body', 'author', 'created_utc']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for subreddit_name in subreddit_names:
            subreddit = reddit.subreddit(subreddit_name)
            total_comments = 0

            while True:
                comments_fetched = 0

                for comment in comment_generator(subreddit, num_comments_per_batch):
                    comment_data = {
                        'id': comment.id,
                        'subreddit': subreddit_name,
                        'body': comment.body.replace('\n', ' '),  # Remove newline characters
                        'author': comment.author.name if comment.author else '[deleted]',
                        'created_utc': int(comment.created_utc)
                    }

                    # Write comment to CSV
                    csv_writer.writerow(comment_data)

                    comments_fetched += 1
                    total_comments += 1

                    if total_comments % num_comments_per_batch == 0:
                        break  # Stop after fetching the desired number of comments

                print(f"Subreddit: {subreddit_name}, Batch Size: {num_comments_per_batch}, Total Comments: {total_comments}")

                # Check if more comments are available
                if comments_fetched < num_comments_per_batch:
                    print(f"   No more comments available for {subreddit_name}.")
                    break

                print(f"   More comments are available for {subreddit_name}. Paginating...")

if __name__ == '__main__':
    subreddit_names = ['announcements']  # Add your list of subreddit names here
    num_comments_per_request = 700

    extract_and_store_comments_csv(subreddit_names, num_comments_per_request)

    print("Comments have been stored in 'new_commments.csv'")
