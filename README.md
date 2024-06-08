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


