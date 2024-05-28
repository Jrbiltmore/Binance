import pandas as pd
import numpy as np
import logging
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketSentimentAnalysis:
    def __init__(self, news_data):
        """
        Initialize the MarketSentimentAnalysis with news data.

        :param news_data: DataFrame containing news data with columns ['date', 'headline', 'source']
        """
        self.news_data = news_data
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        logger.info("MarketSentimentAnalysis initialized with news data")

    def analyze_sentiment_textblob(self, text):
        """
        Analyze sentiment using TextBlob.

        :param text: Text to analyze
        :return: Sentiment polarity score
        """
        analysis = TextBlob(text)
        sentiment_score = analysis.sentiment.polarity
        logger.info(f"TextBlob sentiment score for '{text}': {sentiment_score}")
        return sentiment_score

    def analyze_sentiment_vader(self, text):
        """
        Analyze sentiment using VADER.

        :param text: Text to analyze
        :return: Sentiment polarity score
        """
        sentiment_dict = self.sentiment_analyzer.polarity_scores(text)
        sentiment_score = sentiment_dict['compound']
        logger.info(f"VADER sentiment score for '{text}': {sentiment_score}")
        return sentiment_score

    def calculate_sentiment_scores(self):
        """
        Calculate sentiment scores for all news headlines.

        :return: DataFrame with sentiment scores added
        """
        self.news_data['sentiment_textblob'] = self.news_data['headline'].apply(self.analyze_sentiment_textblob)
        self.news_data['sentiment_vader'] = self.news_data['headline'].apply(self.analyze_sentiment_vader)
        self.news_data['sentiment_avg'] = self.news_data[['sentiment_textblob', 'sentiment_vader']].mean(axis=1)
        logger.info("Calculated sentiment scores for all headlines")
        return self.news_data

    def calculate_average_sentiment(self):
        """
        Calculate the average sentiment score for the entire dataset.

        :return: Average sentiment score
        """
        self.calculate_sentiment_scores()
        average_sentiment = self.news_data['sentiment_avg'].mean()
        logger.info(f"Calculated average sentiment score: {average_sentiment}")
        return average_sentiment

# Example usage:
if __name__ == "__main__":
    # Example news data
    news_data = {
        'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'headline': [
            'Market rallies on positive economic news',
            'Stock prices fall amid geopolitical tensions',
            'Tech stocks soar as new innovations are announced'
        ],
        'source': ['Reuters', 'BBC', 'TechCrunch']
    }
    news_data_df = pd.DataFrame(news_data)

    sentiment_analysis = MarketSentimentAnalysis(news_data_df)
    
    sentiment_scores = sentiment_analysis.calculate_sentiment_scores()
    print(f"Sentiment scores:\n{sentiment_scores}")

    average_sentiment = sentiment_analysis.calculate_average_sentiment()
    print(f"Average sentiment score: {average_sentiment}")
