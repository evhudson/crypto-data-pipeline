import requests
import psycopg2
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# setup logging
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"

def get_connection():
    return psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

def fetch_prices():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    return response.json()

def insert_prices(data):
    conn = get_connection()
    cur = conn.cursor()

    for coin, value in data.items():
        cur.execute(
            "INSERT INTO prices (coin, price_usd, created_at) VALUES (%s, %s, %s)",
            (coin, value["usd"], datetime.utcnow())
        )

    conn.commit()
    cur.close()
    conn.close()

def main():
    try:
        logging.info("Starting ingestion job")

        data = fetch_prices()
        insert_prices(data)

        logging.info("Successfully inserted data")

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to access API endpoint {API_URL}: {e}")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()