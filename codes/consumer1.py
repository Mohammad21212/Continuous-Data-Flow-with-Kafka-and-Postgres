from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer
import json

# Kafka settings
bootstrap_servers = 'kafka1:9091'
input_topic = 'users_info'
output_topic = 'part1'
consumer_group_id = 'python_consumer_group'

def consume_process_produce():
    consumer = KafkaConsumer(
        input_topic,
        bootstrap_servers=bootstrap_servers,
        group_id=consumer_group_id,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    for message in consumer:
        # Process message (add timestamp column)
        data = message.value
        timestamp = datetime.now().isoformat()
        data['timestamp'] = timestamp

        # Publish processed message to output topic
        producer.send(output_topic, value=data)
        print(f"Processed message: {data}")

if __name__ == "__main__":
    consume_process_produce()
