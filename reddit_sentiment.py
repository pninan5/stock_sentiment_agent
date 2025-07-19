import praw
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ==== USER INPUT ====
stock = input("Enter the stock name or ticker (e.g., Tesla or TSLA): ")
search_query = f"{stock} OR {stock.upper()}"


# ==== REDDIT API AUTH ====
reddit = praw.Reddit(
    client_id='CHANGE IT',
    client_secret='CHANGE IT',
    user_agent='StockSentimentAgent',
    username='CHANGE IT',
    password='CHANGE IT'
)

# ==== CONFIG ====
subreddits = ['stocks', 'wallstreetbets', 'investing']

limit = 100  # number of posts per subreddit

# ==== SENTIMENT SETUP ====
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    score = analyzer.polarity_scores(text)
    return score['compound']

# ==== FETCH POSTS ====
posts = []
for sub in subreddits:
    for post in reddit.subreddit(sub).search(search_query, sort='new', limit=limit):
        posts.append([
            post.title,
            post.selftext,
            post.created_utc,
            post.score
        ])

# ==== PROCESS ====
df = pd.DataFrame(posts, columns=['title', 'body', 'timestamp', 'upvotes'])
df['text'] = df['title'] + ' ' + df['body']
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# ==== FILTER: Last 3 Months ====
three_months_ago = pd.Timestamp.now() - pd.DateOffset(months=3)
df = df[df['timestamp'] >= three_months_ago]

# ==== SENTIMENT ====
df['sentiment'] = df['text'].apply(analyze_sentiment)

# ==== SAVE ====
filename = f"reddit_sentiment_{stock.lower()}.csv"
df.to_csv(filename, index=False)
print(f"\nSaved results to {filename}")

# ==== GROUP BY DAY ====
df['date'] = df['timestamp'].dt.date
daily_avg = df.groupby('date')['sentiment'].mean().reset_index()
daily_avg['date'] = pd.to_datetime(daily_avg['date'])

# ==== ROLLING AVERAGE ====
daily_avg['rolling_avg'] = daily_avg['sentiment'].rolling(window=7, min_periods=1).mean()

# ==== PLOT ====
plt.figure(figsize=(12, 6))

# Plot daily sentiment average
sns.lineplot(data=daily_avg, x='date', y='sentiment', label='Daily Avg Sentiment', alpha=0.5)

# Plot 7-day rolling average
sns.lineplot(data=daily_avg, x='date', y='rolling_avg', label='Rolling Avg', linewidth=2)

plt.title(f"{stock.upper()} Sentiment (Last 3 Months) on Reddit")
plt.ylabel("Sentiment Score (-1 to 1)")
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
