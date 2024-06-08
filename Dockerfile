FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY DataEngineering_ETL_AWS-SQS_Postgres.py DataEngineering_ETL_AWS-SQS_Postgres.py

CMD ["python", "DataEngineering_ETL_AWS-SQS_Postgres.py"]
