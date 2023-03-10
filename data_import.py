import os
import yfinance as yf
from multiprocessing import Pool
from tqdm import tqdm
import multiprocessing
import psutil
import pandas as pd

def download_stock_data(ticker):
    try:
        # Use yfinance to fetch the historical stock data for the ticker symbol
        data = yf.download(ticker, start='2010-01-01')

        # Convert ticker symbol to company name
        company_name = yf.Ticker(ticker).info['longName']

        # Add columns for company name, stock name, and date
        stock_name = ticker
        data['company_name'] = company_name
        data['stock_name'] = stock_name
        data = data.reset_index()
        data = data.rename(columns={'Open': 'open_price', 'High': 'high_price', 'Low': 'low_price', 'Close': 'close_price', 'Volume': 'volume', 'Date': 'date'})

        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None


def get_stock_data():
    """
    Fetch historical stock data for a set of companies and their stocks, and combine the data into a single DataFrame.

    Returns:
        pandas.DataFrame: A DataFrame containing the historical stock data for the selected companies and stocks.
    """

    # Check if a cached data file already exists
    cache_file_path = './data/stock_data.csv'
    if os.path.exists(cache_file_path):
        # If it does, load the data from the file and return it as a DataFrame
        print("Loading cached data...")
        all_data = pd.read_csv(cache_file_path)
        all_data['date'] = pd.to_datetime(all_data['date'])
        return all_data

    # Use the search_companies function to get a list of ticker symbols
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']

    # Determine the number of available CPU cores
    num_cores = multiprocessing.cpu_count()

    # Get the amount of available memory in bytes
    available_memory = psutil.virtual_memory().available

    # Calculate the maximum amount of memory per worker process (in bytes)
    max_memory_per_worker = available_memory // num_cores

    # Create a Pool of worker processes to download the stock data in parallel
    with Pool(processes=num_cores, maxtasksperchild=1) as pool:
        # Use tqdm to display a progress bar while the data is being downloaded
        stock_data = list(tqdm(pool.imap(download_stock_data, tickers), total=len(tickers)))

    # Filter out any None values that may have been returned due to errors during the download
    stock_data = [data for data in stock_data if data is not None]

    # Concatenate the list of dataframes into a single dataframe
    all_data = pd.concat(stock_data)

    # Save the data to a cached data file for future use
    os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)
    all_data.to_csv(cache_file_path, index=False)

    return all_data


