import pandas as pd

# Load the data
file_path = 'cleaned_tata_motors_stock_data.csv'
df = pd.read_csv(file_path)

# Convert Date to datetime for clarity (optional)
df['Date'] = pd.to_datetime(df['Date'])

# Select only numeric columns
numeric_df = df.select_dtypes(include=['float64', 'int64'])

# Calculate correlation matrix
correlation_matrix = numeric_df.corr()

print("Correlation Matrix:")
print(correlation_matrix)
