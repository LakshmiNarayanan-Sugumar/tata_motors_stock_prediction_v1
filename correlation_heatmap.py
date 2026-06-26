import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load the cleaned data
df = pd.read_csv('cleaned_tata_motors_stock_data.csv')

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Calculate the correlation matrix without the Date column
correlation_matrix = df.drop(columns=['Date']).corr()

# Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix Heatmap - Tata Motors')
plt.savefig("correlation_heatmap.png")
plt.show()
