import streamlit as st
import pandas as pd
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt


# ==== REDDIT API AUTH ====
reddit = praw.Reddit(
    client_id='CHANGE IT',
    client_secret='CHANGE IT',
    user_agent='StockSentimentAgent',
    username='CHANGE IT',
    password='CHANGE IT'
)
# ==== SETUP ====
analyzer = SentimentIntensityAnalyzer()

def fetch_sentiment(stock):
    query = f"{stock} OR {stock.upper()}"
    subreddits = ['stocks', 'wallstreetbets', 'investing']
    limit = 100
    posts = []
    for sub in subreddits:
        for post in reddit.subreddit(sub).search(query, sort='new', limit=limit):
            posts.append([
                post.title,
                post.selftext,
                post.created_utc,
                post.score
            ])
    df = pd.DataFrame(posts, columns=['title', 'body', 'timestamp', 'upvotes'])
    df['text'] = df['title'] + ' ' + df['body']
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    
    # Filter to last 3 months
    three_months_ago = pd.Timestamp.now() - pd.DateOffset(months=3)
    df = df[df['timestamp'] >= three_months_ago]

    # Sentiment scores
    df['sentiment'] = df['text'].apply(lambda x: analyzer.polarity_scores(x)['compound'])

    # Group by day
    df['date'] = df['timestamp'].dt.date
    daily = df.groupby('date')['sentiment'].mean().reset_index()
    daily['date'] = pd.to_datetime(daily['date'])
    daily['rolling_avg'] = daily['sentiment'].rolling(window=7, min_periods=1).mean()

    return df, daily

# ==== STREAMLIT UI ====
st.title("📈 Reddit Stock Sentiment Analyzer")
stock = st.text_input("Enter a stock name or ticker (e.g., Tesla or AAPL)")

if st.button("Analyze Sentiment") and stock:
    with st.spinner('Fetching Reddit posts and analyzing...'):
        df, daily = fetch_sentiment(stock)

    st.success(f"Analysis complete for: {stock.upper()}")

    # Line chart
    st.subheader("Sentiment Trend (Last 3 Months)")
    st.line_chart(daily.set_index('date')[['sentiment', 'rolling_avg']])

    # Show table
    st.subheader("Top Recent Reddit Posts")
    st.dataframe(df[['timestamp', 'title', 'sentiment']].sort_values('timestamp', ascending=False).head(10))

    # Option to download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, f"{stock.lower()}_sentiment.csv", "text/csv")
