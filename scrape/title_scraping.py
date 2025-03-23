import requests
import csv
import time
import os

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

subreddit = "r/WallStreetBets"
subreddit_url = f'https://www.reddit.com/{subreddit}/hot.json'

num_rows = 0

# Get the current directory and create a path for titles.txt
current_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(current_dir, 'titles.txt')

# Writes titles to a csv called 'titles.txt'
with open(output_file, 'w', newline='', encoding="utf-8") as file:
    file_writer = csv.writer(file)
    file_writer.writerow(['Title'])

    # Fetch hot posts
    response = requests.get(subreddit_url, headers=headers)
    data = response.json()

    # Fetch details for each post
    for post in data['data']['children']:
        title = post['data']['title']
        file_writer.writerow([title])
        num_rows += 1
        print(f"{num_rows} rows written.")

        # Sleep for a short time to avoid hitting rate limits
        time.sleep(1)

print("Done.")