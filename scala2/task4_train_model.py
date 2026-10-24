"""
Task 4: Train a Decision Tree Classifier to Predict Churn or Retention
- Prepare features using VectorAssembler
- Split data into 80% train and 20% test
- Train DecisionTreeClassifier with maxDepth=5
- Show sample predictions
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import mean
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import DecisionTreeClassifier

# Create Spark session
spark = SparkSession.builder \
    .appName("Task4_TrainModel") \
    .master("local[*]") \
    .getOrCreate()

# Load data
df = spark.read.csv("customer_data.csv", header=True, inferSchema=True)

# Handle missing values (Task 2)
mean_freq = df.select(mean("order_frequency")).collect()[0][0]
mean_value = df.select(mean("total_order_value")).collect()[0][0]
df = df.fillna({"order_frequency": mean_freq, "total_order_value": mean_value})

# Encode categorical fields (Task 3)
for col_name in ["location", "membership_type", "gender"]:
    indexer = StringIndexer(inputCol=col_name, outputCol=col_name + "_index")
    df = indexer.fit(df).transform(df)

# Define feature columns
feature_cols = [
    "order_frequency", "total_order_value", "avg_order_value",
    "days_since_last_order", "customer_age", "satisfaction_score",
    "location_index", "membership_type_index", "gender_index"
]

# Assemble features into a single vector
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
df = assembler.transform(df)

# Split data: 80% train, 20% test
train_data, test_data = df.randomSplit([0.8, 0.2], seed=42)

print(f"Training set size: {train_data.count()}")
print(f"Test set size: {test_data.count()}")

# Train Decision Tree Classifier
dt = DecisionTreeClassifier(
    labelCol="churn",
    featuresCol="features",
    maxDepth=5
)
model = dt.fit(train_data)

# Make predictions on test data
predictions = model.transform(test_data)

# Show sample predictions
print("\n=== Sample Predictions ===")
predictions.select("customer_id", "churn", "prediction", "probability").show(10)

# Show feature importances
print("=== Feature Importances ===")
for name, importance in zip(feature_cols, model.featureImportances):
    print(f"  {name}: {importance:.4f}")

spark.stop()
