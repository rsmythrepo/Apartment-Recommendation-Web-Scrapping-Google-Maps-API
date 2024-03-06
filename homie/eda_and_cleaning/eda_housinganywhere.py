import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

# Load your CSV file into a Pandas DataFrame
df = pd.read_csv('../../Data/raw/housinganywhere_data.csv')

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
df['price_per_month'] = df['price_per_month'].str.replace('GBP ', '')
df['price_per_month'] = df['price_per_month'].str.replace('€', '')
df['price_per_month'] = df['price_per_month'].astype(str)
df['price_per_month'] = df['price_per_month'].apply(lambda x: sum(map(int, x.split('-'))) / 2 if '-' in x else int(x))
df['price_per_month'] = df['price_per_month'].astype(int)

# Calculate price per week
df['price_per_week'] = (df['price_per_month'] / 4).round().astype(int)

# Convert Deposit
df['deposit'] = df['deposit'].str.replace('GBP ', '')
# Replace 'Rent' with the corresponding value from 'price_per_month' column
df['deposit'] = df.apply(lambda row: str(row['price_per_month']) if row['deposit'] == 'Rent' else row['deposit'], axis=1)
def extract_and_multiply(string, price):
    match = re.search(r'\d+', string)
    if match:
        numeric_value = int(match.group())
        return numeric_value * price
    else:
        return None

# Apply the function to the 'deposit' and 'price_per_month' columns
df['deposit'] = df.apply(lambda row: extract_and_multiply(row['deposit'], row['price_per_month']) if 'months' in row['deposit'] else row['deposit'], axis=1)

# Replace 'Entire apartment' with 'Apartment' and 'Entire house' with 'House' in the 'house_type' column
df['house_type'] = df['house_type'].replace({'Entire apartment': 'Apartment', 'Entire house': 'House'})

# Define a function to extract the number from dimensions
def extract_numeric(string):
    match = re.search(r'\d+', string)  # Find the first occurrence of one or more digits
    if match:
        return int(match.group())  # Extract and return the numeric value as an integer
    else:
        return None  # Return None if no numeric value is found

# Apply the function to the 'property_description' column
df['dimensions_sq_m'] = df['dimensions'].apply(lambda x: extract_numeric(x))
df.drop("dimensions", axis='columns', inplace=True)

# Define a function to extract the numeric value or set it to 1 if 'Studio'
def extract_bedrooms(string):
    match = re.search(r'\d+', string)  # Find the first occurrence of one or more digits
    if match:
        return int(match.group())  # Extract and return the numeric value as an integer
    elif 'Studio' in string:
        return 1  # Set it to 1 if 'Studio'
    else:
        return None  # Return None if no numeric value is found

# Apply the function to the 'bedrooms' column
df['bedrooms'] = df['bedrooms'].apply(lambda x: extract_bedrooms(x))

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

# Plot the distribution of deposit
plt.figure(figsize=(10, 6))
sns.histplot(df['price_per_month'], bins=20, kde=True)
plt.title('Distribution of Deposit')
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

# Plot the count of bathrooms
plt.figure(figsize=(10, 6))
sns.countplot(data=df.dropna(subset=['bathrooms']), x='bathrooms')
plt.title('Count of Bathrooms')
plt.xlabel('Number of Bathrooms')
plt.ylabel('Count')
plt.show()

# Plot scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(df['bedrooms'], df['price_per_month'], alpha=0.5)
plt.title('Relationship between Bedrooms and Price per Month')
plt.xlabel('Number of Bedrooms')
plt.ylabel('Price per Month')
plt.grid(True)
plt.show()

'''Save the processed data'''
df.to_csv("../../Data/processed/housinganywhere_data.csv")
