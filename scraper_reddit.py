#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import os
import praw
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import re

# Download VADER lexicon if not already present
nltk.download("vader_lexicon")
analyzer = SentimentIntensityAnalyzer()

# Create data folder
os.makedirs("data", exist_ok=True)

# Reddit API credentials from environment variables
reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent=os.environ.get("REDDIT_USER_AGENT")
)

# Search terms to locate Trump nickname threads
search_terms = ["Trump nicknames", "funny names for Trump", "nicknames against Trump"]

nickname_entries = []

for term in search_terms:
    print("Searching Reddit for: {}".format(term))
    for submission in reddit.subreddit("all").search(term, limit=10):
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            text = comment.body.strip()
            if len(text) > 5 and len(text.split()) < 10 and text[0].isupper():
                sentiment_score = analyzer.polarity_scores(text)['compound']
                if sentiment_score >= 0.05:
                    sentiment = "Positive"
                elif sentiment_score <= -0.05:
                    sentiment = "Negative"
                else:
                    sentiment = "Neutral"

                nickname_entries.append({
                    "Nickname": text,
                    "Used By": "Reddit user {}.format(comment.author)",
                    "Context / Explanation": "From Reddit comment in r/{}.format(submission.subreddit.display_name)",
                    "Source Type": "Social Media",
                    "Specific Source Name": "r/{}.format(submission.subreddit.display_name)",
                    "Media Format": "Reddit Comment",
                    "Region / Country": "Unknown",
                    "Language": "English",
                    "Date of First Use": str(pd.to_datetime(comment.created_utc, unit='s').date()),
                    "Popularity (1-5)": 3,
                    "Sentiment": sentiment
                })

# Save to CSV
df = pd.DataFrame(nickname_entries)
df.to_csv("data/nicknames_reddit.csv", index=False)
print("Saved {len(df)} nicknames from Reddit.")

