import json
import psycopg2
import logging
from kafka import KafkaConsumer

# Kafka settings
bootstrap_servers = 'kafka1:9091'
input_topic = 'part2'
consumer_group_id = 'python_consumer_group_3'

# PostgreSQL settings
db_host = 'postgres'
db_port = 5432
db_name = 'dblab'
db_user = 'postgres'
db_password = 'postgres123'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def consume_and_store():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    logger.info("Connected to PostgreSQL successfully.")

    # Initialize Kafka consumer
    consumer = KafkaConsumer(
        input_topic,
        bootstrap_servers=bootstrap_servers,
        group_id=consumer_group_id,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    logger.info("Starting Kafka consumer...")

    # Main loop to consume messages and store in PostgreSQL
    for message in consumer:
        data = message.value

        # Log received data
        logger.info("Received data from Kafka: %s", data)

        # Insert data into PostgreSQL table
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO users_info (id, first_name, last_name, gender, address, post_code, email, username, dob, registered_date, phone, picture, timestamp, labels)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            data['id'], data['first_name'], data['last_name'], data['gender'], data['address'],
            data['post_code'], data['email'], data['username'], data['dob'], data['registered_date'],
            data['phone'], data['picture'], data['timestamp'], data['labels']
        ))
        conn.commit()
        cursor.close()

        # Log successful insertion
        logger.info("Data inserted successfully: %s", data)

    # Close Kafka consumer and PostgreSQL connection
    consumer.close()
    logger.info("Kafka consumer closed.")
    conn.close()
    logger.info("PostgreSQL connection closed.")


if __name__ == "__main__":
    consume_and_store()
