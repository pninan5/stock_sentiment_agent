# AI Stock Sentiment Agent

A Streamlit based analytics app that converts Reddit market chatter into a structured sentiment signal you can explore and export.

Disclaimer: This project is for education and analytics only. It is not financial advice.

---

## What this project does
1. Pulls recent Reddit posts about a stock or company (ticker or keyword)
2. Cleans text and computes sentiment using VADER
3. Aggregates results and visualizes trends (rolling sentiment)
4. Shows sample posts driving sentiment
5. Exports a CSV report for further analysis

---

## Why it matters
Retail sentiment can shift quickly and often contains early signals about product reactions, investor mood, and news digestion. This app helps you:
• Track sentiment trends over time  
• Compare signals across tickers  
• Inspect the posts driving bullish or bearish moves  
• Export structured data for modeling or backtesting  

---

## Core features
• Ticker or keyword search (example: TSLA, NVDA, AAPL)  
• Reddit ingestion via PRAW  
• VADER sentiment scoring per post  
• Rolling sentiment chart  
• Sample post table for interpretability  
• One click CSV export  

---

## How sentiment is computed
VADER outputs positive, negative, neutral proportions and a compound score in the range from minus 1 to plus 1.
This project uses the compound score as the primary sentiment signal.
Common thresholds (tunable):
• Bullish if compound is at least 0.05  
• Bearish if compound is at most minus 0.05  
• Neutral otherwise  

---

## Tech stack
• Python  
• Streamlit  
• PRAW (Reddit API)  
• vaderSentiment (VADER)  
• pandas  
• matplotlib  

---

## Project structure
If your repo layout differs, update the paths below to match.
```
streamlit_app.py
requirements.txt
```

Recommended additions for cleanliness:
```
assets/
  screenshots/
src/
  data_collection.py
  preprocessing.py
  sentiment_scoring.py
  utils.py
```

---

## How to run on Windows
These steps preserve your existing run instructions and make them copy paste friendly.

### Step 1: Clone or download the project
Option A: Git users
```
git clone https://github.com/your-username/stock-sentiment-agent.git
cd stock-sentiment-agent
```

Option B: Manual
• Download the ZIP from GitHub  
• Extract it and open the folder  

### Step 2: Create and activate a virtual environment
```
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install required packages
```
pip install -r requirements.txt
```

If requirements.txt is missing, install manually:
```
pip install streamlit praw pandas matplotlib vaderSentiment
```

### Step 4: Set up Reddit API credentials
1. Visit https://www.reddit.com/prefs/apps  
2. Click Create App and choose script  
3. Fill in:
   • Name: StockSentimentAgent  
   • Redirect URI: http://localhost:8080  
4. Click Create  
5. Copy:
   • client_id  
   • client_secret  
   • username  
   • password  

### Step 5: Insert credentials into the script
Replace the following block in streamlit_app.py:
```python
reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user_agent='StockSentimentAgent',
    username='YOUR_USERNAME',
    password='YOUR_PASSWORD'
)
```

Security note: It is better to load credentials from environment variables (for example, a .env file) and add .env to .gitignore so secrets are not committed.

### Step 6: Run the app
```
streamlit run streamlit_app.py
```

Then open http://localhost:8501 in your browser.

### Step 7: Use the app
• Type a stock name or ticker (example: TSLA)  
• Click Analyze Sentiment  
• Review the rolling sentiment chart  
• Inspect Reddit post samples  
• Download the CSV report  

Optional: update PRAW
```
pip install --upgrade praw
```

---

## Screenshots (recommended for interview readiness)
Add 2 to 3 screenshots and link them here:
• assets/screenshots/dashboard.png  
• assets/screenshots/trend.png  
• assets/screenshots/sample_posts.png  

---

## Limitations and next steps
Limitations:
• Social data can be noisy and biased  
• Sentiment is not the same as price movement  
• Sampling windows and subreddit selection can change results  

Next steps:
• Add spam and bot filtering  
• Add topic clustering (product news vs macro news)  
• Add price data alignment to test predictive value  
• Add alerting when sentiment shifts sharply  

---

## Quick interview talking points
• Built a text to signal pipeline: ingestion, cleaning, scoring, aggregation, dashboard  
• Chose VADER for speed and interpretability on social style language  
• Designed outputs to be actionable: trends plus the posts driving the score  
• Structured so the sentiment model can be swapped later (FinBERT or LLM classifier)
