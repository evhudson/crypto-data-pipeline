import requests
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host="localhost",
    database="crypto_db",
    user="postgres",
    password="7566",
    port="5432"
)

cur = conn.cursor()

url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"
data = requests.get(url).json()

for coin, value in data.items():
    cur.execute(
        "INSERT INTO prices (coin, price_usd, created_at) VALUES (%s, %s, %s)",
        (coin, value["usd"], datetime.utcnow())
    )

conn.commit()
cur.close()
conn.close()

print("Inserted data")