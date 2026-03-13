# Kafka producer - simulates e-commerce order events
from kafka import KafkaProducer
import json, random, time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_order():
    return {
        "order_id": random.randint(10000, 99999),
        "customer_id": random.randint(1, 5000),
        "product_id": random.randint(1, 500),
        "quantity": random.randint(1, 10),
        "price": round(random.uniform(5.0, 500.0), 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

while True:
    order = generate_order()
    producer.send('orders', value=order)
    print(f"Sent: {order}")
    time.sleep(0.1)
