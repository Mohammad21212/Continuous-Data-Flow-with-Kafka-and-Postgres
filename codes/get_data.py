import uuid
import json
import logging
import requests
import base64
from kafka import KafkaProducer
import time

logging.basicConfig(level=logging.INFO)

def get_data():
    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    return res['results'][0]

def format_data(res):
    data = {}
    location = res['location']
    data['id'] = str(uuid.uuid4())
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{location['street']['number']} {location['street']['name']}, {location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = base64.b64encode(requests.get(res['picture']['medium']).content).decode('utf-8')
    return data

def stream_data():
    producer = KafkaProducer(bootstrap_servers=['kafka1:9091'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    curr_time = time.time()

    while True:
        if time.time() > curr_time + 60: #1 minute
            break
        try:
            res = get_data()
            res = format_data(res)
            producer.send('users_info', res)
        except Exception as e:
            logging.error(f'An error occured: {e}')
            continue

if __name__ == "__main__":
    stream_data()
