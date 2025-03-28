import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
file_path = r"C:\Users\narendra\Downloads\SCMS_Delivery_History_Cleaned.csv"

# Step 2: Load the dataset safely with error handling
warnings.filterwarnings('ignore')  # Ignore warnings for a clean output
try:
    data = pd.read_csv(file_path)  # Load the dataset
    if isinstance(data, pd.DataFrame):  # Check if it's loaded correctly
        print("Dataset loaded successfully!")
    else:
        raise ValueError("Data is not in a valid format.")
except Exception as e:
    print(f"Error loading dataset: {e}")
    data = None  # Set to None if loading fails
# Step 3: Proceed only if data is successfully loaded
if isinstance(data, pd.DataFrame):
    df = data.copy() 
df.head()
df.shape
print(df)#show data
print(df.duplicated())#to check duplicates in data
duplicates=df[df.duplicated()]
print(duplicates)#it gives what are the duplictes in data
print(df.info())

# Count the number of duplicate rows in the dataset
duplicate_count = len(data[data.duplicated()])
# Print the total number of duplicate rows
print("Total Duplicate Rows:", duplicate_count)
# Checking the count of missing values in each column
missing_values = data.isnull().sum()
# Display only columns with missing values
missing_values = missing_values[missing_values > 0]
# Print missing values count
print("Missing Values Count in Each Column:\n", missing_values)

# Visualizing the missing values
# Plot heatmap of missing values
sns.heatmap(data.isnull(), cmap="viridis", cbar=False, yticklabels=False)

# Dataset Columns
df.columns
# Dataset Describe
df.describe(include='all')
# Check Unique Values for each variable.
for i in data.columns.tolist():
    print(f"No. of unique values in {i} is {data[i].nunique()}.")
# Write your code to make your dataset analysis ready.
# Create a copy of the current dataset for analysis
df = data.copy()
# Check the number of missing values in the dataset
print("Total Missing Values:", data.isnull().sum().sum())
# Remove duplicate rows to ensure data consistency
data.drop_duplicates(inplace=True)
# Checking the shape of the dataset Before cleaning
print("Dataset Shape Before Cleaning:", df.shape)

unimportant_columns = ["pq_#","fulfill_via","item_description","molecule/test_type","brand",
                       "dosage","dosage_form","pack_price","first_line_designation",
                       "line_item_insurance_usd"]  # Modify based on your dataset

# Dropping the unimportant columns
df = df.drop(columns=unimportant_columns, errors='ignore')

# Display the remaining columns
print("Columns after removing unimportant ones:", df.columns)
print(df.info())

# Assigning orders with missing 'pq_first_sent_to_client_date' to df_missing_date
df_missing_date = df[df["pq_first_sent_to_client_date"].isnull()]
# Assigning orders with valid 'pq_first_sent_to_client_date' to df_valid_orders
df_valid_orders = df[df["pq_first_sent_to_client_date"].notnull()]

# Convert column to datetime format
df["pq_first_sent_to_client_date"] = pd.to_datetime(df["pq_first_sent_to_client_date"])
# Compute median date
pq_first_sent_client_date = df["pq_first_sent_to_client_date"].median()
# Fill null values with median date
df["pq_first_sent_to_client_date"].fillna(pq_first_sent_client_date, inplace=True)
# Print the median date
print(pq_first_sent_client_date)
print(df.info())

# Convert column to datetime format
df["po_sent_to_vendor_date"] = pd.to_datetime(df["po_sent_to_vendor_date"])
# Compute median date
po_vendor_date = df["po_sent_to_vendor_date"].median()
# Fill null values with median date
df["po_sent_to_vendor_date"].fillna(po_vendor_date, inplace=True)
# Print the median date
print(po_vendor_date)
print(df.info())
weight = df["weight_kilograms"].median()
df["weight_kilograms"].fillna(weight, inplace = True)
print(weight)
print(df.info())
freight_cost = df["freight_cost_usd"].median()
df["freight_cost_usd"].fillna(freight_cost, inplace = True)
print(freight_cost)
print(df.info())

#missing values heatmap
plt.figure(figsize=(10,6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title("Missing Values Heatmap")
plt.show()

#distribution of shipment modes
df["shipment_mode"].value_counts().plot(kind="bar", color="skyblue", figsize=(8,5))
plt.title("Distribution of Shipment Modes")
plt.xlabel("Shipment Mode")
plt.ylabel("Count")
plt.show()

#Top 10 vendors
df["vendor"].value_counts().head(10).plot(kind="barh", color="green", figsize=(8,5))
plt.title("Top 10 Vendors")
plt.xlabel("Number of Orders")
plt.ylabel("Vendor")
plt.show()

#Freight cost distribution
sns.histplot(df["freight_cost_usd"], bins=30, kde=True, color="purple")
plt.title("Freight Cost Distribution")
plt.xlabel("Freight Cost (USD)")
plt.show()

#Weight Distribution
sns.boxplot(x=df["weight_kilograms"], color="red")
plt.title("Weight Distribution of Shipments")
plt.xlabel("Weight (Kg)")
plt.show()

#Shipments per Country
df["country"].value_counts().head(10).plot(kind="bar", color="orange", figsize=(8,5))
plt.title("Top 10 Shipment Destinations")
plt.xlabel("Country")
plt.ylabel("Number of Shipments")
plt.show()

#shipment mode vs freight cost
sns.boxplot(x="shipment_mode", y="freight_cost_usd", data=df, palette="Set2")
plt.title("Freight Cost by Shipment Mode")
plt.xlabel("Shipment Mode")
plt.ylabel("Freight Cost (USD)")
plt.show()

#Relationship between weight and freight weight
sns.scatterplot(x=df["weight_kilograms"], y=df["freight_cost_usd"], alpha=0.5, color="blue")
plt.title("Weight vs. Freight Cost")
plt.xlabel("Weight (Kg)")
plt.ylabel("Freight Cost (USD)")
plt.show()

#orders over time
df["po_sent_to_vendor_date"] = pd.to_datetime(df["po_sent_to_vendor_date"])
df.set_index("po_sent_to_vendor_date")["po_/_so_#"].resample("M").count().plot(figsize=(10,5), color="black")
plt.title("Orders Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Orders")
plt.show()

#product category distribution
category_counts = df["product_group"].value_counts()
# Plot pie chart
plt.figure(figsize=(8, 8))
plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140, colors=["lightblue", "lightcoral", "lightgreen", "gold", "violet"])
plt.title("Product Category Distribution")
plt.axis("equal")  # Ensures the pie chart is circular
plt.show()

#average freight cost by country
df.groupby("country")["freight_cost_usd"].mean().sort_values(ascending=False).head(10).plot(kind="barh", color="purple", figsize=(8,5))
plt.title("Top 10 Countries by Average Freight Cost")
plt.xlabel("Average Freight Cost (USD)")
plt.ylabel("Country")
plt.show()

#average weight by shipment mode 
df.groupby("shipment_mode")["weight_kilograms"].mean().plot(kind="bar", color="teal", figsize=(8,5))
plt.title("Average Weight by Shipment Mode")
plt.xlabel("Shipment Mode")
plt.ylabel("Average Weight (Kg)")
plt.show()

#number of shipments per vendor
df["vendor"].value_counts().head(10).plot(kind="barh", color="darkblue", figsize=(8,5))
plt.title("Top 10 Vendors by Shipment Volume")
plt.xlabel("Number of Shipments")
plt.ylabel("Vendor")
plt.show()

# Correlation Heatmap visualization code
# Select only numeric columns for correlation
numeric_df = df.select_dtypes(include=["number"])
# Compute correlation matrix
correlation_matrix = numeric_df.corr()
# Set the figure size
plt.figure(figsize=(12, 6))
# Create the heatmap
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
# Add title
plt.title("Correlation Heatmap of Numerical Features")
# Show plot
plt.show()
# Selecting numerical columns for pair plot
numerical_cols = ["weight_kilograms", "freight_cost_usd", "unit_price", "line_item_quantity", "line_item_value"]
# Creating the Pair Plot
sns.pairplot(df[numerical_cols], diag_kind="kde", corner=True)
# Display the plot
plt.show()

# Saving Cleaned Data
df.to_csv(r"C:\Users\narendra\Downloads\SCMS_Delivery_History_Cleaned_Processed.csv", index=False)
print("Cleaned dataset saved successfully!")

















