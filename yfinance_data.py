import yfinance as yf

ticker = 'TATAMOTORS.NS'
start_date = '2024-01-01'
end_date = '2025-03-28'

try:
    # Ensure Adj Close is available
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
    if data.empty:
        print("No data found. Please check the ticker or date range.")
    else:
        data.to_csv('tata_motors_stock_data.csv')
        print("Data downloaded and saved to 'tata_motors_stock_data.csv'")
except Exception as e:
    print(f"An error occurred: {e}")
