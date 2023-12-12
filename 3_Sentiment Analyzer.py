# Import necessary libraries
import streamlit as st # Streamlit for creating web applications
from newsapi.newsapi_client import NewsApiClient # NewsApiClient for fetching news articles
from nltk.sentiment.vader import SentimentIntensityAnalyzer # SentimentIntensityAnalyzer for sentiment analysis
import matplotlib.pyplot as plt # matplotlib for plotting
import pandas as pd # pandas for data manipulation
from datetime import date, timedelta # datetime for working with dates

# Download 'vader_lexicon' if not available
import nltk

# Download VADER lexicon required for the pre-built sentiment analysis lexicon used by the #SentimentIntensityAnalyzer.
nltk.download('vader_lexicon')

# Initialize SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()


# Giving the page a title
st.title("Sentiment Analysis")

# User input for selecting stocks
stock1 = st.text_input("Choose a Stock for Sentiment Analysis:")
stock2 = st.text_input("Choose another Stock for Comparison:")

# Function to perform sentiment analysis and display results
def perform_sentiment_analysis(stock):
    phrase = stock + " stock" # Phrase is defined to give selected stock as an output
    newsapi = NewsApiClient(api_key='f704389a97e24101834d34232a5da98d') # Gets API-Key
    my_date = date.today() - timedelta(days=7) # Using datetime for the date
    
    # Fetching news articles related to that stock using the News API,
    articles = newsapi.get_everything(q=phrase,
                                      from_param=my_date.isoformat(), # Formating date
                                      language="en", # Defining language
                                      sort_by="relevancy", # Sorting by relevancy
                                      page_size=10)
    # Analyzes the sentiment of each article using VADER sentiment analysis, and returns a #list of sentiment scores.
    sentiments = [] # Sentiemnt as empty list
    # Loop iterates through each article in the  retrieved articles
    for article in articles['articles']: 
        article_content = str(article['title']) + '. ' + str(article['description'])
        #V ADER sentiment analysis tool is applied to analyze the sentiment of the article #content and  compound score, which represents the overall sentiment, is extracted.
        sentiment = sia.polarity_scores(article_content)['compound']
        sentiments.append(sentiment) # Compund sentiment score is appended to empty list

    return sentiments

# Perform sentiment analysis for both stocks
sentiments_stock1 = perform_sentiment_analysis(stock1)
sentiments_stock2 = perform_sentiment_analysis(stock2)

# Display sentiment mean and count
st.write(f"Sentiment Analysis for {stock1}:")
st.write(f"Mean Sentiment: {round(pd.Series(sentiments_stock1).mean(), 4)}")
st.write(f"Number of Articles: {len(sentiments_stock1)}")

# Display the sentiment analysis results for both stocks, including the mean sentiment score and the number of articles considered
st.write(f"Sentiment Analysis for {stock2}:")
st.write(f"Mean Sentiment: {round(pd.Series(sentiments_stock2).mean(), 4)}")
st.write(f"Number of Articles: {len(sentiments_stock2)}")

# Plot sentiment analysis
fig, ax = plt.subplots()
ax.bar([stock1, stock2], [pd.Series(sentiments_stock1).mean(), pd.Series(sentiments_stock2).mean()])
ax.set_xlabel('Stock')
ax.set_ylabel('Sentiment Mean')
ax.set_title('Sentiment Analysis Comparison')
st.pyplot(fig)
