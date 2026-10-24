"""
Task 1: Load Customer Transaction History into Spark DataFrame
- Read the CSV file into a Spark DataFrame
- Display schema, first few rows, and basic stats
"""

from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("Task1_LoadData") \
    .master("local[*]") \
    .getOrCreate()

# Load dataset into Spark DataFrame
df = spark.read.csv("customer_data.csv", header=True, inferSchema=True)

# Display schema
print("=== Schema ===")
df.printSchema()

# Show first 5 rows
print("=== First 5 Rows ===")
df.show(5)

# Basic counts
print(f"Total Records: {df.count()}")
print(f"Total Columns: {len(df.columns)}")
print(f"Column Names: {df.columns}")

# Summary statistics
print("\n=== Summary Statistics ===")
df.describe().show()

spark.stop()
