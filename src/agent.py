import sys
from youtube_api import get_channel_id, get_latest_videos, get_video_comments
from database import create_tables, save_channel, save_video, save_comment
from sentiment import load_sentiment_model, analyze_sentiment

def run_pipeline(channel_input):
    print(f"\n Starting pipeline for: {channel_input}")
    
    # Step 1 - Setup database
    create_tables()
    
    # Step 2 - Get channel
    channel_id = get_channel_id(channel_input)
    save_channel(channel_id, channel_input)
    
    # Step 3 - Get videos
    videos = get_latest_videos(channel_id)
    print(f"Found {len(videos)} videos!")
    
    # Step 4 - Load sentiment model
    model = load_sentiment_model()
    
    # Step 5 - For each video get comments and analyze
    for video in videos:
        video_id = video["snippet"]["resourceId"]["videoId"]
        title = video["snippet"]["title"]
        published_at = video["snippet"]["publishedAt"]
        
        save_video(video_id, channel_id, title, published_at)
        print(f"\n Processing: {title}")
        
        comments = get_video_comments(video_id)
        print(f"Found {len(comments)} comments")
        
        for i, comment in enumerate(comments):
            label, score = analyze_sentiment(model, comment)
            save_comment(f"{video_id}_{i}", video_id, comment, 0, label, score)
        
        print(f"Saved and analyzed all comments!")

if __name__ == "__main__":
    channel = input("Enter YouTube channel handle (e.g. @MrBeast): ")
    run_pipeline(channel)