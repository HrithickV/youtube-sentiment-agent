import sqlite3
import pandas as pd
import os

def create_connection():
    return sqlite3.connect("data/youtube_data.db")

def generate_report():
    conn = create_connection()
    
    query = '''
        SELECT 
            ch.channel_title,
            v.title,
            COUNT(c.comment_id) as total_comments,
            SUM(CASE WHEN c.sentiment_label = 'POSITIVE' THEN 1 ELSE 0 END) as positive,
            SUM(CASE WHEN c.sentiment_label = 'NEGATIVE' THEN 1 ELSE 0 END) as negative
        FROM channels ch
        JOIN videos v ON ch.channel_id = v.channel_id
        JOIN comments c ON v.video_id = c.video_id
        WHERE ch.channel_title != 'Test Video'
        GROUP BY ch.channel_title, v.video_id
        ORDER BY ch.channel_title
    '''
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df["positive_%"] = (df["positive"] / df["total_comments"] * 100).round(2)
    df["negative_%"] = (df["negative"] / df["total_comments"] * 100).round(2)
    
    # Group by channel
    for channel, group in df.groupby("channel_title"):
        print(f"\n{'='*60}")
        print(f" CHANNEL: {channel}")
        print(f"{'='*60}")
        
        print("\n VIDEO WISE SENTIMENT:")
        for _, row in group.iterrows():
            print(f"\n {row['title'][:50]}")
            print(f"     Total Comments : {row['total_comments']}")
            print(f"     Positive     : {row['positive']} ({row['positive_%']}%)")
            print(f"     Negative     : {row['negative']} ({row['negative_%']}%)")
        
        # Channel summary
        total = group["total_comments"].sum()
        positive = group["positive"].sum()
        negative = group["negative"].sum()
        
        print(f"\n CHANNEL SUMMARY:")
        print(f"   Total Comments : {total}")
        print(f"   Overall Positive  : {positive} ({round(positive/total*100, 2)}%)")
        print(f"   Overall Negative  : {negative} ({round(negative/total*100, 2)}%)")
    
    # Save CSV
    os.makedirs("data/exports", exist_ok=True)
    df.to_csv("data/exports/video_report.csv", index=False)
    print("\n Report saved to data/exports/video_report.csv")

if __name__ == "__main__":
    generate_report()