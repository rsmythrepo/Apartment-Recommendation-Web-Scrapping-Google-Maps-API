import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

# Load your CSV file into a Pandas DataFrame
df = pd.read_csv('../../Data/raw/apartmentsanywhere_data.csv')

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
df['price_per_month'] = df['price_per_month'].str.replace('GBP ', '').astype(int)
df['price_per_week'] = (df['price_per_month'] / 4).round().astype(int)

# Define a function to extract the number between "sq ft" and "sq m"

print(df.head())
print(df.info())

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
