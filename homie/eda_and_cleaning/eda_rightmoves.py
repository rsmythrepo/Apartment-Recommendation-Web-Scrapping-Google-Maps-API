import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

# Load your CSV file into a Pandas DataFrame
df = pd.read_csv('../../Data/raw/rightmoves_data.csv')

# Display the first few rows of the dataframe
print(df.head())

# Summary of the dataframe
print(df.info())

# Summary statistics of numerical columns
print(df.describe())

# Check for missing values
print(df.isnull().sum())


'''Cleaning the data'''

# Extract the price from the string and make it an int
df['price_per_month'] = df['price_per_month'].str.replace('£', '').str.replace('pcm', '').str.replace(',', '').astype(int)
df['price_per_week'] = df['price_per_week'].str.replace('£', '').str.replace('pw', '').str.replace(',', '').astype(int)

# Clean deposit
df['deposit'] = df['deposit'].replace('Ask agent', '0')
def clean_and_convert_currency(currency):
    cleaned_currency = currency.replace('£', '').replace(',', '')  # Remove currency symbol and commas
    return int(cleaned_currency)  # Convert to integer

# Apply the function to the 'price' column
df['deposit'] = df['deposit'].apply(lambda x: clean_and_convert_currency(x))
df['deposit'] = df['deposit'].replace(0, None)

# Replace non-numeric values in 'bathrooms' and 'bedrooms' with NaN
df['bathrooms'] = pd.to_numeric(df['bathrooms'], errors='coerce')
df['bedrooms'] = pd.to_numeric(df['bedrooms'], errors='coerce')

df['bathrooms'] = df['bathrooms'].astype('Int64')
df['bedrooms'] = df['bedrooms'].astype('Int64')

# Define a function to extract the number between "sq ft" and "sq m"
def extract_second_number(dimensions):
    # Using regular expression to find the second number
    match = re.search(r'(\d+)\s+sq\s+m', dimensions)
    if match:
        return int(match.group(1))
    else:
        return None

# Apply the extraction function to create a new column
df['dimensions_sq_m'] = df['dimensions'].apply(extract_second_number)
df.drop("dimensions", axis='columns', inplace=True)

print(df.head())
print(df.info())
print(df.describe())

'''Plot the data'''
# Plot the distribution of prices
plt.figure(figsize=(10, 6))
sns.histplot(df['price_per_month'], bins=20, kde=True)
plt.title('Distribution of Price Per Month')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Plot the distribution of prices per week
plt.figure(figsize=(10, 6))
sns.histplot(df['price_per_week'], bins=20, kde=True)
plt.title('Distribution of Price Per Week')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Plot the distribution of dimensions_sq_m
plt.figure(figsize=(10, 6))
sns.histplot(df['dimensions_sq_m'].dropna(), bins=20, kde=True, color='green')
plt.title('Distribution of Dimensions (sq m)')
plt.xlabel('Dimensions (sq m)')
plt.ylabel('Frequency')
plt.show()

# Plot the count of bedrooms
plt.figure(figsize=(10, 6))
sns.countplot(data=df.dropna(subset=['bedrooms']), x='bedrooms')
plt.title('Count of Bedrooms')
plt.xlabel('Number of Bedrooms')
plt.ylabel('Count')
plt.show()

# Plot the count of bathrooms
plt.figure(figsize=(10, 6))
sns.countplot(data=df.dropna(subset=['bathrooms']), x='bathrooms')
plt.title('Count of Bathrooms')
plt.xlabel('Number of Bathrooms')
plt.ylabel('Count')
plt.show()

# Relationship between bedrooms and price

# Drop rows with missing values
df_clean = df.dropna(subset=['bedrooms', 'price_per_month'])

# Plot scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(df_clean['bedrooms'], df_clean['price_per_month'], alpha=0.5)
plt.title('Relationship between Bedrooms and Price per Month')
plt.xlabel('Number of Bedrooms')
plt.ylabel('Price per Month')
plt.grid(True)
plt.show()

print(df.head())
print(df.info())

'''Save the processed data'''
df.to_csv("../../Data/processed/rightmoves_data.csv")




