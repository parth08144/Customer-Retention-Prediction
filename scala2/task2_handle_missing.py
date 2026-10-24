"""
Task 2: Handle Missing Order Frequency and Value Details
- Check for missing values in each column
- Fill missing order_frequency with column mean
- Fill missing total_order_value with column mean
- Verify no missing values remain
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import mean, col, count, when, isnan, isnull

# Create Spark session
spark = SparkSession.builder \
    .appName("Task2_HandleMissing") \
    .master("local[*]") \
    .getOrCreate()

# Load data
df = spark.read.csv("customer_data.csv", header=True, inferSchema=True)

# Check missing values BEFORE handling
print("=== Missing Values BEFORE Handling ===")
for c in df.columns:
    missing_count = df.filter(col(c).isNull() | isnan(col(c))).count()
    if missing_count > 0:
        print(f"  {c}: {missing_count} missing")

# Calculate mean for order_frequency
mean_freq = df.select(mean("order_frequency")).collect()[0][0]
print(f"\nMean order_frequency: {mean_freq:.2f}")

# Calculate mean for total_order_value
mean_value = df.select(mean("total_order_value")).collect()[0][0]
print(f"Mean total_order_value: {mean_value:.2f}")

# Fill missing values with mean
df_clean = df.fillna({
    "order_frequency": mean_freq,
    "total_order_value": mean_value
})

# Verify no missing values remain
print("\n=== Missing Values AFTER Handling ===")
has_missing = False
for c in df_clean.columns:
    missing_count = df_clean.filter(col(c).isNull() | isnan(col(c))).count()
    if missing_count > 0:
        print(f"  {c}: {missing_count} missing")
        has_missing = True

if not has_missing:
    print("  No missing values remain!")

# Show cleaned data
print("\n=== Cleaned Data (first 5 rows) ===")
df_clean.show(5)

spark.stop()
