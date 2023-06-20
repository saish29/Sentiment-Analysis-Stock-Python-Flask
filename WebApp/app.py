import flask
from flask import Flask, render_template # for web app
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import json # for graph plotting in website
# NLTK VADER for sentiment analysis
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# for extracting data from finviz
finviz_url = 'https://finviz.com/quote.ashx?t='

def get_news(ticker):
    url = finviz_url + ticker
    req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}) 
    response = urlopen(req)    
    # Read the contents of the file into 'html'
    html = BeautifulSoup(response, features="html.parser")
    # Find 'news-table' in the Soup and load it into 'news_table'
    news_table = html.find(id='news-table')
    return news_table
	
# parse news into dataframe

def parse_news(news_table):
    parsed_news = []
    
    for x in news_table.findAll('tr'):
        # check if 'a' tag is present in the 'tr' tag
        if x.a is not None:
            # read the text from 'a' tag into text
            text = x.a.get_text() 
            # splite text in the td tag into a list 
            date_scrape = x.td.text.split()
            # if the length of 'date_scrape' is 1, load 'time' as the only element
            if len(date_scrape) == 1:
                time = date_scrape[0]
            # else load 'date' as the 1st element and 'time' as the second    
            else:
                date = date_scrape[0]
                time = date_scrape[1]
            # Append ticker, date, time and headline as a list to the 'parsed_news' list
            parsed_news.append([date, time, text])        
    # Set column names
    columns = ['date', 'time', 'headline']
    # Convert the parsed_news list into a DataFrame called 'parsed_and_scored_news'
    parsed_news_df = pd.DataFrame(parsed_news, columns=columns)        
    # Create a pandas datetime object from the strings in 'date' and 'time' column
    parsed_news_df['datetime'] = pd.to_datetime(parsed_news_df['date'] + ' ' + parsed_news_df['time'])
    
    return parsed_news_df
        
def score_news(parsed_news_df):
    # Instantiate the sentiment intensity analyzer
    vader = SentimentIntensityAnalyzer()
    
    # Iterate through the headlines and get the polarity scores using vader
    scores = parsed_news_df['headline'].apply(vader.polarity_scores).tolist()

    # Convert the 'scores' list of dicts into a DataFrame
    scores_df = pd.DataFrame(scores)

    # Join the DataFrames of the news and the list of dicts
    parsed_and_scored_news = parsed_news_df.join(scores_df, rsuffix='_right')
    
            
    parsed_and_scored_news = parsed_and_scored_news.set_index('datetime')
    
    parsed_and_scored_news = parsed_and_scored_news.drop(['date', 'time'], axis = 1)    
        
    parsed_and_scored_news = parsed_and_scored_news.rename(columns={"compound": "sentiment_score"})

    return parsed_and_scored_news

def plot_hourly_sentiment(parsed_and_scored_news, ticker):
    # Group by date and ticker columns from parsed_and_scored_news and calculate the mean
    mean_scores = parsed_and_scored_news.resample('H').mean()
    
    # Create a new column called 'color' that maps positive sentiment scores to green and negative scores to red
    mean_scores['color'] = np.where(mean_scores['sentiment_score'] > 0, 'green', 'red')

    # Plot a bar chart with plotly, setting the color of each bar based on the 'color' column
    fig = px.bar(mean_scores, x=mean_scores.index, y='sentiment_score', title=ticker + ' Hourly Sentiment Scores',
             color='color', color_discrete_map={'green': 'green', 'red': 'red'})
    # Update the x and y axis labels
    fig.update_xaxes(title_text='Date and Time')
    fig.update_yaxes(title_text='Sentiment Score')

    # Add custom labels for positive and negative sentiment scores
    fig.update_layout(legend=dict(title='', orientation='h', y=1.1, x=0.5, xanchor='center'),
                    coloraxis_colorbar=dict(title='Sentiment', tickvals=[-1, 0, 1],
                                            ticktext=['Negative', 'Neutral', 'Positive'],
                                            tickmode='array', ticks='outside'))

    # Remove the legend
    fig.update_layout(showlegend=False)


    return fig

def plot_daily_sentiment(parsed_and_scored_news, ticker):
   
    # Group by date and ticker columns from scored_news and calculate the mean
    mean_scores = parsed_and_scored_news.resample('D').mean()

    # Plot a bar chart with plotly
    fig = px.bar(mean_scores, x=mean_scores.index, y='sentiment_score', title = ticker + ' Daily Sentiment Scores', color_discrete_sequence = ["coral"])
    fig.update_xaxes(title_text='Date and Time')
    fig.update_yaxes(title_text='Sentiment Score')

    # fig.show()
    
    return fig


app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sentiment', methods = ['POST'])
def sentiment():

	ticker = flask.request.form['ticker'].upper()
	news_table = get_news(ticker)
	parsed_news_df = parse_news(news_table)
	parsed_and_scored_news = score_news(parsed_news_df)
	fig_hourly = plot_hourly_sentiment(parsed_and_scored_news, ticker)
	fig_daily = plot_daily_sentiment(parsed_and_scored_news, ticker)

	graphJSON_hourly = json.dumps(fig_hourly, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON_daily = json.dumps(fig_daily, cls=plotly.utils.PlotlyJSONEncoder)
	
	header= "Hourly and Daily Sentiment of {} Stock".format(ticker)
	description = """
	The above chart averages the sentiment scores of {} stock hourly and daily.
	The table below gives each of the most recent headlines of the stock and the negative, neutral, positive and an aggregated sentiment score.
	The news headlines are obtained from the FinViz website.
	Sentiments are given by the nltk.sentiment.vader Python library.
    """.format(ticker)
	return render_template('sentiment.html',graphJSON_hourly=graphJSON_hourly, graphJSON_daily=graphJSON_daily, header=header,table=parsed_and_scored_news.to_html(classes='data'),description=description)



        
if __name__ == '__main__':
    app.run()