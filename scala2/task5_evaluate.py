"""
Task 5: Evaluate Model Using Accuracy, Precision, and Recall
- Run the full pipeline (load, clean, encode, train)
- Evaluate predictions using MulticlassClassificationEvaluator
- Print accuracy, precision, and recall scores
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import mean
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Create Spark session
spark = SparkSession.builder \
    .appName("Task5_Evaluate") \
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

# Assemble features (Task 4)
feature_cols = [
    "order_frequency", "total_order_value", "avg_order_value",
    "days_since_last_order", "customer_age", "satisfaction_score",
    "location_index", "membership_type_index", "gender_index"
]
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
df = assembler.transform(df)

# Split and train (Task 4)
train_data, test_data = df.randomSplit([0.8, 0.2], seed=42)
dt = DecisionTreeClassifier(labelCol="churn", featuresCol="features", maxDepth=5)
model = dt.fit(train_data)
predictions = model.transform(test_data)

# === Evaluation ===
print("=== Model Evaluation ===\n")

# Accuracy
evaluator_acc = MulticlassClassificationEvaluator(
    labelCol="churn", predictionCol="prediction", metricName="accuracy"
)
accuracy = evaluator_acc.evaluate(predictions)
print(f"Accuracy:  {accuracy:.4f}")

# Precision
evaluator_prec = MulticlassClassificationEvaluator(
    labelCol="churn", predictionCol="prediction", metricName="weightedPrecision"
)
precision = evaluator_prec.evaluate(predictions)
print(f"Precision: {precision:.4f}")

# Recall
evaluator_rec = MulticlassClassificationEvaluator(
    labelCol="churn", predictionCol="prediction", metricName="weightedRecall"
)
recall = evaluator_rec.evaluate(predictions)
print(f"Recall:    {recall:.4f}")

# Confusion-style breakdown
print("\n=== Prediction Breakdown ===")
predictions.groupBy("churn", "prediction").count().show()

spark.stop()
