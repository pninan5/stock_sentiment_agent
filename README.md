## 💻 How to Run the Stock Sentiment Analyzer on Your System

> These instructions are for Windows users with Python installed.

---

### ✅ Step 1: Clone or Download the Project

Option A: Git users
```bash
git clone https://github.com/your-username/stock-sentiment-agent.git
cd stock-sentiment-agent
```

Option B: Manual
- Download the ZIP file from GitHub
- Extract it and open the folder

---

### ✅ Step 2: Create and Activate a Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate
```

---

### ✅ Step 3: Install All Required Packages

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:

```bash
pip install streamlit praw pandas matplotlib vaderSentiment
```

---

### ✅ Step 4: Set Up Reddit API Credentials

1. Visit: [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Click **Create App** → Choose **script**
3. Fill in:
    - Name: StockSentimentAgent
    - Redirect URI: `http://localhost:8080`
4. Click **Create**
5. Copy:
    - `client_id`
    - `client_secret`
    - `username`
    - `password`

---

### ✅ Step 5: Insert Credentials into the Script

Replace the following block in `streamlit_app.py`:

```python
reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user_agent='StockSentimentAgent',
    username='YOUR_USERNAME',
    password='YOUR_PASSWORD'
)
```

---

### ✅ Step 6: Run the App

```bash
streamlit run streamlit_app.py
```

Visit [http://localhost:8501](http://localhost:8501) in your browser.

---

### ✅ Step 7: Use the App

- Type a stock name or ticker (e.g., `TSLA`)
- Click **Analyze Sentiment**
- View the rolling sentiment chart
- Scroll to view Reddit post samples
- Download the CSV report

---

### 🔁 Optional: Update PRAW or Any Package

```bash
pip install --upgrade praw
```