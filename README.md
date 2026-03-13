Real-Time E-Commerce Data Pipeline on AWS
An end-to-end streaming data pipeline that ingests, processes, and models real-time e-commerce order events — built with Kafka, PySpark, Airflow, dbt, and Amazon Redshift.
---
Architecture
```
[Order Events] → [Kafka] → [PySpark on EMR] → [S3 Raw] → [dbt] → [Redshift] → [QuickSight]
                                                               ↑
                                                          [Airflow DAGs]
```
> See `architecture/pipeline_diagram.png` for the full visual.
---
Tech Stack
Layer	Tool
Ingestion	Apache Kafka
Processing	PySpark on AWS EMR
Storage	Amazon S3
Orchestration	Apache Airflow
Transformation	dbt (data build tool)
Warehouse	Amazon Redshift
Visualization	AWS QuickSight
Language	Python 3.10, SQL
---
Project Structure
```
ecommerce-pipeline/
├── kafka/
│   ├── producer.py          # Simulates order event stream
│   └── consumer.py          # Kafka consumer → S3 sink
├── spark/
│   └── transform_orders.py  # PySpark job on EMR
├── dbt/
│   ├── models/
│   │   ├── staging/         # Raw source models
│   │   └── marts/
│   │       ├── orders.sql
│   │       ├── customers.sql
│   │       └── products.sql
│   └── tests/               # dbt data quality tests
├── airflow/
│   └── dags/
│       └── pipeline_dag.py  # Daily orchestration DAG
├── architecture/
│   └── pipeline_diagram.png
└── README.md
```
---
Pipeline Overview
1. Ingestion — Kafka
A Python producer simulates 100K+ daily order events (order ID, customer ID, product, quantity, timestamp) and publishes them to a Kafka topic with Avro schema validation.
```python
# kafka/producer.py (snippet)
producer.send('orders', value=order_event)
```
2. Processing — PySpark on EMR
A PySpark job reads from the Kafka consumer output in S3, applies transformations (deduplication, type casting, enrichment), and writes Parquet files back to S3.
```python
# spark/transform_orders.py (snippet)
df = spark.read.json("s3://bucket/raw/orders/")
df_clean = df.dropDuplicates(["order_id"]) \
             .withColumn("order_date", to_date("timestamp"))
df_clean.write.parquet("s3://bucket/processed/orders/")
```
Processing time reduced by ~40% compared to a pandas baseline on the same dataset.
3. Transformation — dbt
Three dbt marts are built on top of the processed Parquet data loaded into Redshift staging tables:
`orders` — order-level metrics (revenue, status, fulfillment time)
`customers` — customer lifetime value, order frequency
`products` — top sellers, inventory movement
All models have full dbt test coverage (not null, unique, referential integrity).
4. Orchestration — Airflow
A daily Airflow DAG chains the pipeline steps with failure alerting via email/Slack:
```
start → kafka_consumer → emr_spark_job → s3_sensor → dbt_run → dbt_test → end
```
5. Analytics — Redshift + QuickSight
Final mart tables are queried in Redshift and visualized in AWS QuickSight dashboards covering:
Daily/weekly revenue trends
Customer cohort retention
Top products by region
---
Getting Started
Prerequisites
AWS account with EMR, S3, Redshift, and QuickSight access
Python 3.10+
Docker (for local Kafka and Airflow)
dbt CLI
Setup
```bash
# Clone the repo
git clone https://github.com/yourusername/ecommerce-pipeline.git
cd ecommerce-pipeline

# Install Python dependencies
pip install -r requirements.txt

# Start Kafka locally
docker-compose up -d kafka zookeeper

# Run the producer
python kafka/producer.py

# Trigger Airflow DAG (or run steps manually)
airflow dags trigger ecommerce_pipeline
```
---
Key Results
Streamed and processed 100K+ simulated daily order events
PySpark job runs ~40% faster than pandas baseline
3 dbt marts with full test coverage (zero failures)
Automated daily runs with Airflow DAGs and failure alerting
End-to-end pipeline runs in under 15 minutes
---
What I Learned
Designing fault-tolerant Kafka producers with schema validation
Tuning PySpark jobs for performance on AWS EMR
Building modular, tested dbt models following best practices
Orchestrating multi-step pipelines with Airflow dependencies and sensors
---
License
MIT
