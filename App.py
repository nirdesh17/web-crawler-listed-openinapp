import os
import csv
import json
import googleapiclient.discovery

import os
from dotenv import load_dotenv


load_dotenv()


# Set up the API client
api_service_name = "youtube"
api_version = "v3"
api_key = os.getenv("API_KEY")
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

def fetch_youtube_videos(keyword, num_results):
    # Call the search.list method to search for videos with the keyword
    search_response = youtube.search().list(
        q=keyword,
        part="snippet",
        maxResults=num_results
    ).execute()

    videos = []

    # Iterate through the search results and retrieve video details
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            video = {
                "Title": search_result["snippet"]["title"],
                "Video ID": search_result["id"]["videoId"],
                "URL": f"https://www.youtube.com/watch?v={search_result['id']['videoId']}"
            }
            videos.append(video)

    return videos

def save_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def save_to_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Usage example
keyword = "openinapp"
num_results = 10000

youtube_videos = fetch_youtube_videos(keyword, num_results)

# Save to CSV file
csv_filename = "videos.csv"
save_to_csv(youtube_videos, csv_filename)
print(f"Videos saved to {csv_filename}")

# Save to JSON file
json_filename = "videos.json"
save_to_json(youtube_videos, json_filename)
print(f"Videos saved to {json_filename}")
