"""
Task 6: Visualize Retention Rates Across Different Membership Levels
- Calculate retention rate (1 - churn_rate) per membership type
- Display a simple bar chart using matplotlib
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import mean, col
import matplotlib.pyplot as plt

# Create Spark session
spark = SparkSession.builder \
    .appName("Task6_Visualize") \
    .master("local[*]") \
    .getOrCreate()

# Load data
df = spark.read.csv("customer_data.csv", header=True, inferSchema=True)

# Calculate churn rate per membership type
retention_df = df.groupBy("membership_type").agg(
    mean("churn").alias("churn_rate")
).toPandas()

# Calculate retention rate
retention_df["retention_rate"] = 1 - retention_df["churn_rate"]
retention_df = retention_df.sort_values("membership_type")

# Print results
print("=== Retention Rates by Membership Type ===")
print(retention_df[["membership_type", "retention_rate", "churn_rate"]].to_string(index=False))

# Simple bar chart
plt.figure(figsize=(8, 5))
bars = plt.bar(
    retention_df["membership_type"],
    retention_df["retention_rate"],
    color=["#2196F3", "#4CAF50", "#FFC107"]
)

# Add value labels on bars
for bar, rate in zip(bars, retention_df["retention_rate"]):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
             f'{rate:.2%}', ha='center', fontsize=12)

plt.xlabel("Membership Type")
plt.ylabel("Retention Rate")
plt.title("Customer Retention Rates by Membership Level")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("retention_chart.png")
plt.show()

print("\nChart saved as retention_chart.png")

spark.stop()
