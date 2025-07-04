import pandas as pd

# Load the CSV file
df = pd.read_csv('tata_motors_news.csv')
print("Column Names:", df.columns)


print("Initial Data Shape:", df.shape)

# Step 1: Remove Duplicates
df = df.drop_duplicates()
print("After Removing Duplicates:", df.shape)

# Step 2: Handle Missing Values
# Fill missing descriptions with 'No Description Available'
df['Description'].fillna('No Description Available', inplace=True)

# Fill missing titles with 'No Title Available'
df['Title'].fillna('No Title Available', inplace=True)

# Step 3: Clean Text Data
def clean_text(text):
    text = str(text)
    text = text.replace('\n', ' ').replace('\r', ' ') # Remove newlines
    text = text.strip() # Remove leading/trailing spaces
    return text

df['Description'].fillna('No Description Available', inplace=True)
df['Description'] = df['Description'].apply(clean_text)


# Step 4: Save Cleaned Data
df.to_csv('cleaned_tata_motors_news.csv', index=False)
print("Data cleaning completed. Cleaned data saved to cleaned_tata_motors_news.csv")
