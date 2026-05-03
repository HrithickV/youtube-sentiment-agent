import os 
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')

def get_youtube_client():
    youtube = build("youtube", "v3", developerKey=API_KEY)
    return youtube


def get_channel_id(channel_input):
    youtube = get_youtube_client()
    request = youtube.search().list(
        part="snippet",
        q=channel_input,
        type = "channel",
        maxResults = 1
    )
    response = request.execute()
    channel_id = response["items"][0]["snippet"]["channelId"]
    return channel_id
    

def get_latest_videos(channel_id):
    youtube = get_youtube_client()

    channel_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id

    ).execute()

    uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    request = youtube.playlistItems().list(
    part = "snippet",
    playlistId = uploads_playlist_id,
    maxResults = 10
    )
    response = request.execute()
    return response["items"] 




def get_video_comments(video_id):
    youtube = get_youtube_client()
    request = youtube.commentThreads().list(
        part = "snippet",
        videoId = video_id,
        maxResults = 100
    )
    response = request.execute()

    comments = []
    for item in response["items"]:
        comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment_text)
    return comments





if __name__ == "__main__":
    client = get_youtube_client()
    print("YouTube client created successfully!")

    channel_id = get_channel_id("@MrBeast")
    print(f"Channel ID: {channel_id}")

    videos = get_latest_videos(channel_id)
    print(f"Found{len(videos)} videos!")
    print(f"First Video: {videos[0]['snippet']['title']}")

    video_id = videos[0]['snippet']['resourceId']['videoId']
    comments = get_video_comments(video_id)
    print(f"found {len(comments)} comments!!")
    print(f"first comment: {comments[0]}")



