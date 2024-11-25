from googlesearch import search
import requests
from bs4 import BeautifulSoup
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import time

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()


# Function to clean text
def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters
    return text.lower().strip()


# Function to scrape article content
def scrape_google_results(query, max_results=10):
    articles = []
    print(f"Searching Google for: {query}")

    try:
        count = 0
        for url in search(query, lang="en"):
            try:
                response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")

                # Extract the article title and text
                title = soup.find("title").text if soup.find("title") else "No Title"
                paragraphs = soup.find_all("p")
                content = " ".join(p.text for p in paragraphs)
                sentiment = sia.polarity_scores(clean_text(content))["compound"]

                articles.append({
                    "url": url,
                    "title": title,
                    "content": content[:500],  # Save only first 500 characters
                    "sentiment": sentiment,
                })

                print(f"Scraped: {title} | Sentiment: {sentiment}")
                count += 1
                if count >= max_results:
                    break  # Limit to max_results

                time.sleep(1)  # Be polite to servers
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                continue

    except Exception as e:
        print(f"Error searching Google: {e}")

    return articles


# Comprehensive Keywords for Balanced Sentiment
keywords = [
    # Positive/neutral keywords
    "nuclear power", "nuclear reactors", "uranium",
    "power plants", "clean energy", "advanced nuclear energy",

    # Negative keywords
    "nuclear power is bad", "dangers of nuclear power", "radiation",
    "Chernobyl", "Fukushima", "why nuclear power is dangerous",
    "nuclear disaster", "radiation sickness", "nuclear accident"
]

# Compile search queries for the last 5 years
queries = [f"{keyword} after:2018" for keyword in keywords]

# Scrape articles from Google search results
all_articles = []

for query in queries:
    articles = scrape_google_results(query, max_results=10)  # Limit to 10 results per query
    all_articles.extend(articles)

# Save results to a DataFrame and export to CSV
if all_articles:
    file_name = "google_news_sentiment_analysis_no_location.csv"
    df = pd.DataFrame(all_articles)
    df.to_csv(file_name, index=False)
    print(f"Sentiment analysis complete. Results saved to '{file_name}' in the local directory.")
else:
    print("No articles were collected. Please check the scraping logic.")
