import finnhub

def search_companies(search_term, pe_ratio=None, roe=None):
    """
    Search for companies based on the given search term and additional criteria.

    Args:
        search_term (str): The search term to use to filter companies.
        pe_ratio (float): The maximum P/E ratio to filter companies by.
        roe (float): The minimum ROE to filter companies by.

    Returns:
        list: A list of ticker symbols for the filtered companies.
    """

    # Set up a client for the Finnhub API using your API key
    finnhub_client = finnhub.Client(api_key='cfnbiipr01qokr93c96gcfnbiipr01qokr93c970')

    # Set up the headers dictionary to include the X-Finnhub-Secret field
    headers = {
        'X-Finnhub-Secret': 'cfnbiipr01qokr93c980'
    }

    # Retrieve a list of stock symbols that match the search term, including the headers dictionary in the request
    result = finnhub_client.stock_symbols(query=search_term, headers=headers)

    # Extract the ticker symbols from the search result
    tickers = [entry['symbol'] for entry in result]

    # Calculate the P/E ratio and ROE for each company (if specified)
    if pe_ratio is not None or roe is not None:
        pe_ratio_dict = {}
        roe_dict = {}
        for ticker in tickers:
            # Use the Financials function from finnhub to get the financial statement data for the ticker symbol, including the headers dictionary in the request
            financials = finnhub_client.financials_reported(symbol=ticker, freq='annual', headers=headers)
            # Calculate the P/E ratio and ROE
            if financials:
                eps = financials[0]['epsBasic']
                net_income = financials[0]['netIncome']
                shareholders_equity = financials[0]['totalStockholdersEquity']
                if eps and net_income and shareholders_equity:
                    pe_ratio_dict[ticker] = float(eps) / float(net_income)
                    roe_dict[ticker] = float(net_income) / float(shareholders_equity)

        # Filter the list of companies based on the P/E ratio and ROE (if specified)
        filtered_tickers = tickers
        if pe_ratio is not None:
            filtered_tickers = [ticker for ticker in filtered_tickers if pe_ratio_dict.get(ticker, float('inf')) <= pe_ratio]
        if roe is not None:
            filtered_tickers = [ticker for ticker in filtered_tickers if roe_dict.get(ticker, 0) >= roe]
    else:
        filtered_tickers = tickers

    # Return the list of filtered ticker symbols
    return filtered_tickers
