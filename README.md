# Crypto Data Pipeline

## Overview

This project is an end-to-end data engineering pipeline that ingests cryptocurrency market data from the CoinGecko API, stores it in PostgreSQL, performs analytical transformations using SQL, and generates an interactive dashboard for visualization.

The pipeline tracks Bitcoin, Ethereum, and Solana prices over time, enabling historical analysis and trend monitoring.

## Architecture

```text
CoinGecko API
       │
       ▼
 Python ETL Pipeline
       │
       ▼
 PostgreSQL Database
       │
       ▼
 SQL Analytics Views
       │
       ▼
 Plotly Dashboard
```

## Features

* Automated cryptocurrency price ingestion
* PostgreSQL time-series storage
* Historical price tracking
* SQL analytical views
* 7-period moving average calculations
* Interactive Plotly dashboard
* Environment variable based configuration

## Tech Stack

* Python
* PostgreSQL
* psycopg2
* requests
* Plotly
* python-dotenv

## Database Schema

### prices

| Column     | Type               | Description              |
| ---------- | ------------------ | ------------------------ |
| id         | SERIAL PRIMARY KEY | Unique record identifier |
| coin       | TEXT               | Cryptocurrency name      |
| price_usd  | DOUBLE PRECISION   | Price in USD             |
| created_at | TIMESTAMP          | Ingestion timestamp      |

### Indexes

```sql
CREATE INDEX idx_prices_coin_timestamp
ON prices (coin, created_at DESC);
```

## Analytics

The project includes SQL-based analytical views that calculate rolling metrics such as:

* 7-period moving averages
* Historical price trends
* Time-series analysis

Example query:

```sql
SELECT
    coin,
    AVG(price_usd) AS average_price
FROM prices
GROUP BY coin;
```

## Dashboard

The dashboard visualizes:

* Bitcoin price trends
* Ethereum price trends
* Solana price trends
* 7-period moving averages
* Last 24 hours of market activity

The dashboard is generated automatically as `dashboard.html`.

## Installation

### Clone the repository

```bash
git clone https://github.com/evhudson/crypto-data-pipeline.git
cd crypto-data-pipeline
```

### Install dependencies

```bash
pip3 install -r requirements.txt
```

### Configure environment variables

Create a `.env` file:

```env
DB_HOST=localhost
DB_NAME=crypto_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

## Running the Pipeline

Run the ingestion pipeline:

```bash
python3 ingest.py
```

Generate the dashboard:

```bash
python3 dashboard.py
```

Open `dashboard.html` in a browser to view the dashboard.

## Future Improvements

* Automated scheduling with Airflow
* Data quality testing
* Containerization with Docker
* dbt transformation layer
* Cloud data warehouse integration
* Spark-based processing

```
```
