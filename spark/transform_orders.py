# PySpark transformation job on AWS EMR
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, col

spark = SparkSession.builder.appName("OrderTransform").getOrCreate()

df = spark.read.json("s3://your-bucket/raw/orders/")

df_clean = df.dropDuplicates(["order_id"]) \
             .withColumn("order_date", to_date(col("timestamp"))) \
             .filter(col("quantity") > 0) \
             .filter(col("price") > 0)

df_clean.write.mode("overwrite").parquet("s3://your-bucket/processed/orders/")

print(f"Processed {df_clean.count()} records")
spark.stop()
