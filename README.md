# Sentiment Analysis Stock Using NLTK and Flask

This is a GitHub project that focuses on sentiment analysis of stock tickers using Natural Language Toolkit (NLTK) and Flask. The project utilizes Beautiful Soup to scrape the top headlines from the Fviz website, applies NLTK's VADER sentiment analysis to these headlines, and provides hourly and daily sentiment analysis for different stock tickers. A Flask web application is developed to display the sentiment analysis results using Plotly.

## Table of Contents

- [Sentiment Analysis Stock Using NLTK and Flask](#sentiment-analysis-stock-using-nltk-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
## Introduction

Sentiment analysis plays a crucial role in understanding the overall sentiment of news headlines related to stocks. By scraping the top headlines from the Fviz website, this project uses NLTK's VADER sentiment analysis to determine the sentiment (positive, negative, or neutral) of each headline. The sentiment analysis results are then presented in an intuitive web application built with Flask and Plotly.

## Installation

To run this project locally, please follow the steps below:

1. Clone this GitHub repository to your local machine:

```bash
git clone https://github.com/saish29/Sentiment-Analysis-Stock-Python-Flask
```
2. Change into the project directory:

```bash
cd Sentiment-Analysis-Stock-Python-Flask/WebApp
```

3. Install the required dependencies using pip:

```bash
pip install -r requrirements.txt
```

4. Run The Flask App

```bash
python app.py
```

his will start the Flask development server.

5. Open your web browser and visit [http://localhost:5000](http://localhost:5000) to access the web application.

Note: Ensure you have Python and pip installed on your system before proceeding with the installation.

## Usage

After following the installation steps mentioned above, you can use the web application to perform sentiment analysis on stock tickers. Here's a brief overview of the usage:

1. Upon accessing the web application, you will see a form where you can enter the stock ticker symbol.

2. Enter the desired stock ticker symbol, such as AAPL for Apple Inc., and select the time frame (hourly or daily) for sentiment analysis.

3. Click the "Submit" button to initiate the sentiment analysis process.

4. The web application will display the sentiment analysis results in the form of visualizations created using Plotly.

5. You can repeat the process for different stock ticker symbols or time frames to analyze the sentiment of various stocks.

## Project Structure

The project structure is as follows:

- `app.py`: This file contains the Flask application code, including the routes and logic for sentiment analysis.

- `templates/`: This directory contains the HTML templates used by the Flask application to render the web pages.

- `static/`: This directory contains static files such as CSS stylesheets and JavaScript files used by the web application.

- `requirements.txt`: This file lists the required Python packages and their versions for this project.

