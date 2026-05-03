import sqlite3
import pandas as pd
import os

def create_connection():
    return sqlite3.connect("data/youtube_data.db")

def generate_video_report():
    conn = create_connection()
    
    query = '''
        SELECT 
            v.title,
            COUNT(c.comment_id) as total_comments,
            SUM(CASE WHEN c.sentiment_label = 'POSITIVE' THEN 1 ELSE 0 END) as positive,
            SUM(CASE WHEN c.sentiment_label = 'NEGATIVE' THEN 1 ELSE 0 END) as negative
        FROM videos v
        JOIN comments c ON v.video_id = c.video_id
        GROUP BY v.video_id
    '''
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df["positive_%"] = (df["positive"] / df["total_comments"] * 100).round(2)
    df["negative_%"] = (df["negative"] / df["total_comments"] * 100).round(2)
    
    os.makedirs("data/exports", exist_ok=True)
    df.to_csv("data/exports/video_report.csv", index=False)
    
    print("\n VIDEO WISE SENTIMENT REPORT")
    print("="*60)
    for _, row in df.iterrows():
        print(f"\n {row['title'][:50]}")
        print(f"   Total Comments : {row['total_comments']}")
        print(f"   Positive    : {row['positive']} ({row['positive_%']}%)")
        print(f"   Negative    : {row['negative']} ({row['negative_%']}%)")
    
    return df

def generate_channel_report(df):
    total = df["total_comments"].sum()
    positive = df["positive"].sum()
    negative = df["negative"].sum()
    
    print("\n CHANNEL WISE SENTIMENT SUMMARY")
    print("="*60)
    print(f"Total Comments Analyzed : {total}")
    print(f"Overall Positive     : {positive} ({round(positive/total*100, 2)}%)")
    print(f"Overall Negative     : {negative} ({round(negative/total*100, 2)}%)")

if __name__ == "__main__":
    df = generate_video_report()
    generate_channel_report(df)
    print("\n Report saved to data/exports/video_report.csv")