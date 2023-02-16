# import requests
# import json

# url = 'https://finance.yahoo.com/quote/AAPL/history?p=AAPL'
# response = requests.get(url)
# data = json.loads(response.text)

import yfinance as yf
import pandas as pd

# Define a list of ticker symbols for the companies you want to retrieve data for
tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'FB']

# Create an empty DataFrame to store the data
df = pd.DataFrame()

# Loop through each ticker symbol and retrieve historical data using the yfinance library
for ticker in tickers:
    # Use the Ticker function from yfinance to get the historical data for the ticker symbol
    stock_data = yf.Ticker(ticker).history(period='max')
    # Add a new column to the DataFrame with the ticker symbol
    stock_data['Ticker'] = ticker
    # Append the data for this ticker to the main DataFrame
    df = df.append(stock_data)

# Reset the index of the DataFrame
df = df.reset_index()

# Print the DataFrame
print(df)
