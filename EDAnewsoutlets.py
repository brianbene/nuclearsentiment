import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_name = "news_sentiment_analysis_FINAL.csv"
df = pd.read_csv(file_name)

# Inspect the data
print("First 5 rows of the dataset:")
print(df.head())
print("\nSummary statistics:")
print(df.describe())

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Descriptive Statistics for Sentiment
print("\nDescriptive statistics for sentiment scores:")
print(df["sentiment"].describe())

# Sentiment Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df["sentiment"], kde=True, bins=20, color="blue")
plt.title("Sentiment Distribution")
plt.xlabel("Sentiment Score")
plt.ylabel("Frequency")
plt.show()

# Sentiment by Source
if "source" in df.columns:
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="source", y="sentiment", palette="Set2")
    plt.title("Sentiment by News Source")
    plt.xlabel("News Source")
    plt.ylabel("Sentiment Score")
    plt.xticks(rotation=45)
    plt.show()

# Time Series Analysis
if "created" in df.columns:
    # Convert 'created' column to datetime
    df["created"] = pd.to_datetime(df["created"], errors="coerce")
    df = df.dropna(subset=["created"])  # Drop rows with invalid dates
    df.set_index("created", inplace=True)

    # Resample and calculate mean sentiment over time
    sentiment_trend = df.resample("M")["sentiment"].mean()
    plt.figure(figsize=(12, 6))
    plt.plot(sentiment_trend, marker="o", linestyle="-", color="green")
    plt.title("Sentiment Trend Over Time")
    plt.xlabel("Time")
    plt.ylabel("Average Sentiment Score")
    plt.grid()
    plt.show()

# Source vs Sentiment Count
if "source" in df.columns:
    plt.figure(figsize=(12, 6))
    source_counts = df.groupby("source")["sentiment"].count().sort_values(ascending=False)
    sns.barplot(x=source_counts.index, y=source_counts.values, palette="viridis")
    plt.title("Number of Articles by News Source")
    plt.xlabel("News Source")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.show()
