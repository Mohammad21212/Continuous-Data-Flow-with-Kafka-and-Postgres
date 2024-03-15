import json
import random
from kafka import KafkaConsumer, KafkaProducer

# Kafka settings
bootstrap_servers = 'kafka1:9091'
input_topic = 'part1'
output_topic = 'part2'
consumer_group_id = 'python_consumer_group_2'

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
        # Process message (add new column, e.g., labels)
        data = message.value
        labels = random.choices(['label1', 'label2', 'label3'], k=1)[0]
        data['labels'] = labels

        # Publish processed message to output topic
        producer.send(output_topic, value=data)
        print(f"Processed message: {data}")

if __name__ == "__main__":
    consume_process_produce()
