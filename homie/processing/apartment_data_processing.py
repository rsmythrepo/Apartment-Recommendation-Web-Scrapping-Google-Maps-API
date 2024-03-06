import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

# Load rightmove apartments
df1 = pd.read_csv('../../Data/processed/housinganywhere_data.csv')

# Load housing anywhere apartments
df2 = pd.read_csv('../../Data/processed/rightmoves_data.csv')

# Merge the data
frames = [df1, df2]
merged_df = pd.concat(frames, ignore_index=True)
merged_df = merged_df.drop(columns=['Unnamed: 0.1'])
merged_df = merged_df.rename(columns={'Unnamed: 0': 'urls'})

# Fix furnished type and let_type
merged_df.loc[merged_df['let_type'] == 'Furnished', 'furnish_type'] = 'Furnished'
merged_df.loc[merged_df['let_type'] == 'Furnished', 'let_type'] = None

merged_df.loc[merged_df['let_type'] == 'Unfurnished', 'furnish_type'] = 'Unfurnished'
merged_df.loc[merged_df['let_type'] == 'Unfurnished', 'let_type'] = None

merged_df.loc[merged_df['let_type'] == 'Furnished or unfurnished, landlord is flexible', 'furnish_type'] = 'Furnished or unfurnished, landlord is flexible'
merged_df.loc[merged_df['let_type'] == 'Furnished or unfurnished, landlord is flexible', 'let_type'] = None

print(merged_df.head())
print(merged_df.info())

'''Plot the data'''
# Plot the distribution of prices
plt.figure(figsize=(10, 6))
sns.histplot(merged_df['price_per_month'], bins=20, kde=True)
plt.title('Distribution of Price Per Month')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Plot the distribution of prices per week
plt.figure(figsize=(10, 6))
sns.histplot(merged_df['price_per_week'], bins=20, kde=True)
plt.title('Distribution of Price Per Week')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Plot the distribution of deposit
plt.figure(figsize=(10, 6))
sns.histplot(merged_df['price_per_month'], bins=20, kde=True)
plt.title('Distribution of Deposit')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Plot the distribution of dimensions_sq_m
plt.figure(figsize=(10, 6))
sns.histplot(merged_df['dimensions_sq_m'].dropna(), bins=20, kde=True, color='green')
plt.title('Distribution of Dimensions (sq m)')
plt.xlabel('Dimensions (sq m)')
plt.ylabel('Frequency')
plt.show()

# Plot scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(merged_df['bedrooms'], merged_df['price_per_month'], alpha=0.5)
plt.title('Relationship between Bedrooms and Price per Month')
plt.xlabel('Number of Bedrooms')
plt.ylabel('Price per Month')
plt.grid(True)
plt.show()

'''Save the processed data'''
merged_df.to_csv("../../Data/processed/all_apartment_data.csv")