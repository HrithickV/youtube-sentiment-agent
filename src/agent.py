import sys
import sqlite3
from youtube_api import get_channel_id, get_latest_videos, get_video_comments
from database import create_tables, save_channel, save_video, save_comment
from sentiment import load_sentiment_model, analyze_sentiment

def clear_database():
    conn = sqlite3.connect("data/youtube_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comments")
    cursor.execute("DELETE FROM videos")
    cursor.execute("DELETE FROM channels")
    conn.commit()
    conn.close()
    print("Database cleared!")

def run_pipeline(channel_input):
    print(f"\n Starting pipeline for: {channel_input}")
    
    clear_database()
    create_tables()
    
    channel_id = get_channel_id(channel_input)
    save_channel(channel_id, channel_input)
    
    videos = get_latest_videos(channel_id)
    print(f" Found {len(videos)} videos!")
    
    model = load_sentiment_model()
    
    for video in videos:
        video_id = video["snippet"]["resourceId"]["videoId"]
        title = video["snippet"]["title"]
        published_at = video["snippet"]["publishedAt"]
        
        save_video(video_id, channel_id, title, published_at)
        print(f"\n📹 Processing: {title}")
        
        comments = get_video_comments(video_id)
        print(f" Found {len(comments)} comments")
        
        for i, comment in enumerate(comments):
            label, score = analyze_sentiment(model, comment)
            save_comment(f"{video_id}_{i}", video_id, comment, 0, label, score)
        
        print(f" Saved and analyzed all comments!")

if __name__ == "__main__":
    channel = input("Enter YouTube channel handle (e.g. @MrBeast): ")
    run_pipeline(channel)