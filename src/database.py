import sqlite3
import os


def create_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/youtube_data.db")
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS channels(
            channel_id TEXT PRIMARY KEY,
            channel_title TEXT
        )''')
    
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS videos(
            video_id TEXT PRIMARY KEY,
            Channel_id TEXT,
            title TEXT,
            published_at TEXT
                   ) ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments(
            comment_id TEXT PRIMARY KEY,
            video_id TEXT,
            comment_text TEXT,
            like_count INTEGER,
            sentiment_label TEXT,
            sentiment_score REAL
                   )''')
    
    conn.commit()
    conn.close()
    print("Tables created successfully")

if __name__ == "__main__":
    create_tables()
    
def save_channel(channel_id, channel_title):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
           INSERT OR IGNORE INTO channels (channel_id, channel_title)
           values(?, ?)
    ''', (channel_id, channel_title))
    conn.commit()
    conn.close()
    print(f"Channel saved: {channel_title} ")

def save_video(video_id, channel_id, title, published_at):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO videos (video_id, channel_id, title, published_at)
        VALUES (?, ?, ?, ?)
    ''', (video_id, channel_id, title, published_at))
    conn.commit()
    conn.close()

def save_comment(comment_id, video_id, comment_text, like_count, sentiment_label, sentiment_score):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO comments (comment_id, video_id, comment_text, like_count, sentiment_label, sentiment_score)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (comment_id, video_id, comment_text, like_count, sentiment_label, sentiment_score))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    
    # Test saving data
    save_channel("UCX6OQ3DkcsbYNE6H8uQQuVA", "MrBeast")
    save_video("abc123", "UCX6OQ3DkcsbYNE6H8uQQuVA", "Test Video", "2024-01-01")
    save_comment("comment1", "abc123", "This is amazing!", 10)
    print("All data saved successfully!")