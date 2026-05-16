import psycopg2
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="crypto_db",
        user="postgres",
        password="7566",
        port="5432"
    )

def fetch_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT coin, price_usd, created_at
        FROM prices
        WHERE created_at > NOW() - INTERVAL '24 hours'
        ORDER BY created_at ASC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def build_dashboard():
    rows = fetch_data()

    # Organise by coin
    coins = {"bitcoin": {"times": [], "prices": []},
             "ethereum": {"times": [], "prices": []},
             "solana":   {"times": [], "prices": []}}

    for coin, price, ts in rows:
        if coin in coins:
            coins[coin]["times"].append(ts)
            coins[coin]["prices"].append(price)

    colors = {"bitcoin": "#f7931a", "ethereum": "#627eea", "solana": "#9945ff"}
    labels = {"bitcoin": "Bitcoin (BTC)", "ethereum": "Ethereum (ETH)", "solana": "Solana (SOL)"}

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        subplot_titles=[labels[c] for c in ["bitcoin", "ethereum", "solana"]],
        vertical_spacing=0.08
    )

    for i, coin in enumerate(["bitcoin", "ethereum", "solana"], start=1):
        fig.add_trace(
            go.Scatter(
                x=coins[coin]["times"],
                y=coins[coin]["prices"],
                mode="lines",
                name=labels[coin],
                line=dict(color=colors[coin], width=1.5),
                hovertemplate="<b>%{y:$,.2f}</b><br>%{x}<extra></extra>"
            ),
            row=i, col=1
        )

    fig.update_layout(
        title=dict(text="Crypto Price Dashboard — Last 24 Hours", font=dict(size=22)),
        height=800,
        template="plotly_dark",
        showlegend=True,
        legend=dict(orientation="h", y=-0.05),
        margin=dict(t=80, b=60)
    )

    fig.update_yaxes(tickprefix="$", tickformat=",.0f")

    fig.write_html("dashboard.html")
    print("Dashboard saved! Open dashboard.html in your browser.")

if __name__ == "__main__":
    build_dashboard()