import pandas as pd

# Load the CSV, skipping the first 2 rows
df = pd.read_csv('tata_motors_stock_data.csv', skiprows=2)

# Rename the columns correctly
df.columns = ['Date', 'Price', 'Adj Close', 'Close', 'High', 'Low', 'Volume']

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Remove invalid dates
df = df[~df['Date'].isna()]

# Save cleaned data
df.to_csv('cleaned_tata_motors_stock_data.csv', index=False)

print("Data cleaned and saved as 'cleaned_tata_motors_stock_data.csv'.")
