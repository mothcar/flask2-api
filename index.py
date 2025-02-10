from flask import Flask
# import pandas as pd
import FinanceDataReader as fdr

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'
def analyze_kospi_movement(start_date, end_date):
    """
    Analyzes the movement of KOSPI stock prices between open and close for given tickers.

    Args:
        start_date (str): Start date for the analysis (YYYY-MM-DD).
        end_date (str): End date for the analysis (YYYY-MM-DD).

    Returns:
        dict: A dictionary where keys are stock codes and values are dictionaries
              of date: 'Up'/'Dn'/'Eq'.
    """
    # '', '', '', '' 
    # kospi_list = fdr.StockListing('KOSPI')
    kospi_list = fdr.DataReader('101530,005935,034020,005690', start_date, end_date)
    results = {}

    #for code in kospi_list['Code']:
    for code in kospi_list:
        try:
            df = fdr.DataReader(code, start_date, end_date)
            if df.empty:
                print(f"No data for {code} in the specified date range.")
                continue

            results[code] = {}

            for index, row in df.iterrows():
                date_str = index.strftime('%Y-%m-%d')
                open_price = row['Open']
                close_price = row['Close']

                if close_price > open_price:
                    results[code][date_str] = 'Up'
                elif close_price < open_price:
                    results[code][date_str] = 'Dn'
                else:
                   results[code][date_str] = 'Eq'

        except Exception as e:
            print(f"Error processing {code}: {e}")
            continue

    return results


# Example usage:
start_date = "2025-01-01"
end_date = "2025-02-05"
# kospi_analysis = analyze_kospi_movement(start_date, end_date)
# print(kospi_analysis)

@app.route('/about')
def about():
    kospi_analysis = analyze_kospi_movement(start_date, end_date)
    # print(kospi_analysis)
    return kospi_analysis