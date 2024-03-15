# Continuous Data Flow with Kafka and Postgres

## Description

This mini-project focuses on creating a continuous flow of information using site data. The project utilizes Linux command line, Kafka, and Postgres for implementing a three-stage data processing pipeline.

## Prerequisites

- Linux environment
- Docker
- Docker Compose

## Installation and Setup

1. Clone this repository:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Start Kafka and Postgres services using Docker Compose:

   ```bash
   docker-compose up -d
   ```

3. Now open new terminal in same directory for Run Python scripts:

   ```bash
   docker-compose exec python_service bash
   ```

4. Now open another terminal window in same directory for PostgreSQL:

   ```bash
   docker-compose exec -it postgres bash
   ```

5. Access KafkaHQ web interface to monitor Kafka topics and messages.

   ```url
   http://localhost:9200
   ```

## Usage

#### Linux

1. First we need to install Dependencies such as pip, python3, kafka-python Library, requests Library, ... .

    ```bash
    apt update
    apt install -y python3 python3-pip
    pip install --upgrade kafka-python
    pip install requests
    pip install psycopg2-binary
    ```

2. you can see cronjob for run automatically get_data.py by this commamd:

    ```bash
    crontab -l
    ```

3. If it was not set, you can do it with these commands:

   ```markdown
   apt update
   apt install nano
   export EDITOR=vim
   crontab -e
   * * * /usr/bin/python3 /codes/get_data.py
   ```

4. Run the Kafka consumers:

- First consumer (consumer1.py): Receives data from the initial topic, adds a timestamp column, and sends the output to a new topic.
- Second consumer (consumer2.py): Receives data from the first topic, adds new columns (e.g., labels), and sends the output to a new topic.
- Third consumer (consumer3.py): Receives the enriched data and saves it in Postgres.(after create table users_info in postgres run this file.)

```bash
 python3 consumer1.py
 python3 consumer2.py
 python3 consumer3.py
```



#### PostgreSQL

1. First we should get access to postgres user:

   ```bash
   su postgres
   ```

2. Setting Up Full Backup + WAL Archiving :

   ```bash
   pg_basebackup -D /backup/standalone-"$(date +%Y-%m-%dT%H-%M)" -c fast -P -R 
   ```

   open postgresql.conf in db_data folder to change it:

   ```conf
   wal_level = replica			# line 211
   archive_mode = on		    # line 258
   archive_command = 'test ! -f /archive/%f && cp %p /archive/%f'		# line 263
   ```

3. Now we should work with psql:

   ```bash
   psql
   ```

3. Go to dblab Database:

   ```bash
   \c dblab
   ```

4. Create table users_info:

   ```query
   CREATE TABLE users_info (
       id UUID PRIMARY KEY,
       first_name VARCHAR(50),
       last_name VARCHAR(50),
       gender VARCHAR(10),
       address VARCHAR(255),
       post_code VARCHAR(20),
       email VARCHAR(100),
       username VARCHAR(50),
       dob DATE,
       registered_date TIMESTAMP,
       phone VARCHAR(20),
       picture TEXT,
       timestamp TIMESTAMP,
       labels VARCHAR(50)
   );
   
   ```

5. Observe rows:

6. ```markdown
   SELECT * FROM users_info;
   ```

#### NoCodeDB

I tried to add this to my project, but due to the fact that I could not establish an interface between the Postgres database with this, I could not, but I tried my best.

