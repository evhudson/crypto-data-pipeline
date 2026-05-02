import requests
import psycopg2
from datetime import datetime
import logging

# setup logging
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"

def fetch_prices():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    return response.json()

def insert_prices(data):
    conn = psycopg2.connect(
        host="localhost",
        database="crypto_db",
        user="postgres",
        password="7566",
        port="5432"
    )
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