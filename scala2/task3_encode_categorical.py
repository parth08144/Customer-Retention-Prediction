"""
Task 3: Encode Categorical Fields (Location, Membership Type, Gender)
- Use StringIndexer to convert categorical columns to numeric indices
- Show original vs encoded values
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import mean
from pyspark.ml.feature import StringIndexer

# Create Spark session
spark = SparkSession.builder \
    .appName("Task3_EncodeCategorical") \
    .master("local[*]") \
    .getOrCreate()

# Load data
df = spark.read.csv("customer_data.csv", header=True, inferSchema=True)

# Handle missing values first (from Task 2)
mean_freq = df.select(mean("order_frequency")).collect()[0][0]
mean_value = df.select(mean("total_order_value")).collect()[0][0]
df = df.fillna({"order_frequency": mean_freq, "total_order_value": mean_value})

# Categorical columns to encode
categorical_cols = ["location", "membership_type", "gender"]

print("=== Encoding Categorical Fields ===\n")

for col_name in categorical_cols:
    # Create StringIndexer for each column
    indexer = StringIndexer(inputCol=col_name, outputCol=col_name + "_index")
    df = indexer.fit(df).transform(df)
    print(f"Encoded: {col_name} -> {col_name}_index")

# Show original vs encoded values
print("\n=== Location Encoding ===")
df.select("location", "location_index").distinct().show()

print("=== Membership Type Encoding ===")
df.select("membership_type", "membership_type_index").distinct().show()

print("=== Gender Encoding ===")
df.select("gender", "gender_index").distinct().show()

# Show sample of encoded data
print("=== Sample Encoded Data ===")
df.select("customer_id", "location", "location_index",
          "membership_type", "membership_type_index",
          "gender", "gender_index").show(10)

spark.stop()
