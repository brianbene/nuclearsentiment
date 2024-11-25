import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load the dataset
df = pd.read_excel("nuclear_power_sentiment.xlsx")

# Convert 'created' to datetime
df["created"] = pd.to_datetime(df["created"], unit="s")

# Inspect the dataset
print("First 5 rows of the dataset:")
print(df.head())
print("\nSummary statistics:")
print(df.describe())

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Sentiment distribution
plt.figure(figsize=(10, 6))
sns.histplot(df["sentiment"], kde=True, bins=20, color="blue")
plt.title("Sentiment Distribution")
plt.xlabel("Sentiment Score")
plt.ylabel("Frequency")
plt.show()

# Sentiment by Score
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="score", y="sentiment", hue="sentiment", palette="coolwarm")
plt.title("Sentiment vs. Score")
plt.xlabel("Score")
plt.ylabel("Sentiment Score")
plt.show()

# Time-based Sentiment Trends
plt.figure(figsize=(12, 6))
sentiment_trend = df.resample("M", on="created")["sentiment"].mean()
plt.plot(sentiment_trend, marker="o", linestyle="-", color="green")
plt.title("Sentiment Trend Over Time")
plt.xlabel("Time")
plt.ylabel("Average Sentiment Score")
plt.grid()
plt.show()

# Keyword Analysis: Count occurrences of 'nuclear' in text
df["keyword_count"] = df["text"].str.lower().str.count("nuclear")
plt.figure(figsize=(10, 6))
sns.histplot(df["keyword_count"], bins=15, kde=False, color="purple")
plt.title("Keyword Frequency Distribution ('nuclear')")
plt.xlabel("Keyword Count")
plt.ylabel("Frequency")
plt.show()

# Sentiment by Keyword Frequency
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="keyword_count", y="sentiment", palette="viridis")
plt.title("Sentiment by Keyword Frequency")
plt.xlabel("Keyword Count")
plt.ylabel("Sentiment Score")
plt.show()
