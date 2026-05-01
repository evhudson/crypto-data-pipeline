# crypto-data-pipeline
# Crypto Data Pipeline

## Overview
This project is an end-to-end data pipeline that ingests cryptocurrency price data from a public API and stores it in PostgreSQL for time-series analysis.

The pipeline fetches real-time prices for Bitcoin, Ethereum, and Solana using the CoinGecko API and writes them into a relational database for querying and analysis.

---

## Architecture

Data flows through the system as follows:

API (CoinGecko) → Python Ingestion Script → PostgreSQL Database → SQL Queries

---

## Tech Stack

- Python
- PostgreSQL
- psycopg2
- requests

---

## Database Schema

Table: `prices`

| Column      | Type                | Description                  |
|------------|---------------------|------------------------------|
| id         | SERIAL PRIMARY KEY  | Unique record ID             |
| coin       | TEXT                | Cryptocurrency name          |
| price_usd  | DOUBLE PRECISION    | Price in USD                 |
| created_at | TIMESTAMP           | Time of data ingestion       |

Index:
- `(coin, created_at DESC)` for efficient time-series queries

---

## How It Works

1. Fetches crypto prices from CoinGecko API
2. Parses JSON response
3. Inserts records into PostgreSQL
4. Stores timestamped price data for historical tracking

---

## How to Run

### 1. Install dependencies
```bash
pip3 install requests psycopg2-binary