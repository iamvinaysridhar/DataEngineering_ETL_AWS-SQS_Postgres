## Overview: Step-by-Step Solution
This application reads JSON data from an AWS SQS queue, masks PII fields, and writes the transformed data to a PostgreSQL database.

1. Setup the Environment
Ensure you have Docker, Docker Compose, AWS CLI Local, and PSQL installed.

Install Docker

Install Docker Compose

Install AWS CLI Local: pip install awscli-local

Install PSQL

2. Create Docker Compose File
Create a docker-compose.yml file to set up the Postgres and Localstack services.

3. Application Development
Create a Python script to handle the ETL process.
Directory Structure, requirements.txt, Dockerfile, DataEngineering_ETL_AWS-SQS_Postgres.py

4. Running the Application
   
Build and Run Docker Containers:

bash
docker-compose up -d

Build and Run the ETL Application:

bash
docker build -t etl .
docker run --network="host" etl

5. Verification
   
Check Messages in SQS:

bash
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue

Verify Data in Postgres:

bash
psql -d postgres -U postgres -p 5432 -h localhost -W
SELECT * FROM user_logins;




   Configuration:-

SQS Queue URL: http://localhost:4566/000000000000/login-queue

Postgres Credentials:

Database: postgres

User: postgres

Password: postgres

Host: localhost

Port: 5432

Assumptions:-
1. The SQS queue and Postgres database are accessible locally through Docker containers.
2. Sensitive PII fields like device_id and ip are hashed using SHA-256 to easily identify duplicates.

Future Improvements:-

1. Improve error handling and logging mechanisms.
2. Use environment variables instead of hard-coding configuration values.
3. Write unit and integration tests for better code coverage and quality.
4. Set up a CI/CD pipeline like Jenkins for automated builds and deployments.

Scaling:-
1. For handling large volumes of data, use a scalable message broker like Kafka instead of SQS.
2. Implement batch processing of messages for improved throughput.
3. Optimize database operations by indexing frequently queried columns and tables.

PII Recovery:-
1. Store original unhashed PII data in an encrypted form for potential recovery later.
2. If PII recovery is needed, use a reversible hashing technique like bcrypt instead of SHA-256.

