# sportsradar-api-connector

## Context
Downloads data feed from the sportradar API and stores it in a local database.

## How to run?

To start up the mysql container:
```shell
docker compose up
```

To ingest data:
```shell
pip install -r requirements.txt
python3 ingest.py
```