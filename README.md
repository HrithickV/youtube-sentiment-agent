# AI Agentic YouTube Comment Sentiment Analysis

## What this project does
Automatically fetches YouTube comments, analyzes sentiment using AI, and generates reports.

## Tech Stack
- Python, YouTube Data API, Hugging Face, SQLite, Pandas

## Setup
1. Clone repo
2. Create virtual environment: `python3.11 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install: `pip install -r requirements.txt`
5. Add `.env` file with `YOUTUBE_API_KEY=your_key`

## Run
```bash
python3 src/agent.py
python3 src/report.py
```

## Results
- Video wise sentiment report
- Channel wise sentiment summary
- CSV export in data/exports/