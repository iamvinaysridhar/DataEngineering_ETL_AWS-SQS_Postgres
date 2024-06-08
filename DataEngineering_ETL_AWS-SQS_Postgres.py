# Importing all the required libraries
import boto3
import hashlib
import json
import psycopg2
from datetime import datetime

# SQS and Postgres connections
SQS_QUEUE_URL = 'http://localhost:4566/000000000000/login-queue'
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

def hash_data(data):
    """
    We need to perform hashing to hide personal identifiable information (PII). The fields `device_id` and `ip` should be masked
    Hashes the input data using SHA-256 algorithm
    """
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def process_sqs_message(message, cursor):
    """
    Processes SQS message and inserts the data into the PostgreSQL database.
    """
    try:
        data = json.loads(message['Body'])
        user_id = data['user_id']
        device_type = data['device_type']
        hashed_ip = hash_data(data['ip'])
        hashed_device_id = hash_data(data['device_id'])
        locale = data['locale']
        app_version = int(data['app_version'])
        create_date = datetime.strptime(data['create_date'], '%Y-%m-%d').date()

        insert_query = """
            INSERT INTO user_logins (user_id, device_type, hashed_ip, hashed_device_id, locale, app_version, create_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, device_type, hashed_ip, hashed_device_id, locale, app_version, create_date))
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error processing message: {message}. Error: {e}")

def main():
    """
    Main function to read messages from SQS and insert them into the PostgreSQL database.
    """
    conn = None
    cursor = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname = DB_NAME,
            user = DB_USER,
            password = DB_PASSWORD,
            host = DB_HOST,
            port = DB_PORT
        )
        cursor = conn.cursor()

        # Connect to SQS
        sqs = boto3.client('sqs', endpoint_url = 'http://localhost:4566')
        response = sqs.receive_message(QueueUrl = SQS_QUEUE_URL, MaxNumberOfMessages = 10)

        # Process each message
        if 'Messages' in response:
            for message in response['Messages']:
                process_sqs_message(message, cursor)
            conn.commit()

    except psycopg2.Error as db_err:
        print(f"Database error: {db_err}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    main()
