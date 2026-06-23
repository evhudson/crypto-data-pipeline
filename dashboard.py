import psycopg2
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# Database Connection
#
# Creates a connection to PostgreSQL.
# This allows Python to run SQL queries against
# the crypto_db database.
# --------------------------------------------------
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )


# --------------------------------------------------
# Fetch Data
#
# Pulls the last 24 hours of cryptocurrency data
# from the moving_average_7 view.
#
# We use the view instead of the raw table because
# it already contains our analytical calculation:
# the 7-period moving average.
# --------------------------------------------------
def fetch_data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            coin,
            price_usd,
            moving_avg_7,
            created_at
        FROM moving_average_7
        WHERE created_at > NOW() - INTERVAL '24 hours'
        ORDER BY created_at ASC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


# --------------------------------------------------
# Dashboard Builder
#
# Main function that:
#
# 1. Pulls data from PostgreSQL
# 2. Organizes it by coin
# 3. Builds Plotly charts
# 4. Saves dashboard.html
# --------------------------------------------------
def build_dashboard():

    rows = fetch_data()

    # --------------------------------------------------
    # Data Structure
    #
    # Store each coin separately.
    #
    # Example:
    #
    # coins["bitcoin"]["prices"]
    # coins["bitcoin"]["ma7"]
    #
    # This makes plotting much easier later.
    # --------------------------------------------------
    coins = {
        "bitcoin": {
            "times": [],
            "prices": [],
            "ma7": []
        },
        "ethereum": {
            "times": [],
            "prices": [],
            "ma7": []
        },
        "solana": {
            "times": [],
            "prices": [],
            "ma7": []
        }
    }

    # --------------------------------------------------
    # Load SQL results into our dictionary
    #
    # Each row contains:
    #
    # coin
    # price_usd
    # moving_avg_7
    # created_at
    # --------------------------------------------------
    for coin, price, ma7, ts in rows:

        if coin in coins:
            coins[coin]["times"].append(ts)
            coins[coin]["prices"].append(price)
            coins[coin]["ma7"].append(ma7)

    # --------------------------------------------------
    # Chart Colors
    #
    # Give each cryptocurrency its own color.
    # --------------------------------------------------
    colors = {
        "bitcoin": "#f7931a",
        "ethereum": "#627eea",
        "solana": "#9945ff"
    }

    # --------------------------------------------------
    # Display Labels
    #
    # More readable chart titles.
    # --------------------------------------------------
    labels = {
        "bitcoin": "Bitcoin (BTC)",
        "ethereum": "Ethereum (ETH)",
        "solana": "Solana (SOL)"
    }

    # --------------------------------------------------
    # Create Dashboard Layout
    #
    # 3 charts stacked vertically.
    #
    # Row 1 = Bitcoin
    # Row 2 = Ethereum
    # Row 3 = Solana
    # --------------------------------------------------
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        subplot_titles=[
            labels["bitcoin"],
            labels["ethereum"],
            labels["solana"]
        ],
        vertical_spacing=0.08
    )

    # --------------------------------------------------
    # Add Charts
    #
    # For each coin:
    #
    # Line 1 = Actual Price
    # Line 2 = 7-period Moving Average
    #
    # The moving average smooths out
    # short-term price fluctuations.
    # --------------------------------------------------
    for i, coin in enumerate(
        ["bitcoin", "ethereum", "solana"],
        start=1
    ):

        # Price Line
        fig.add_trace(
            go.Scatter(
                x=coins[coin]["times"],
                y=coins[coin]["prices"],
                mode="lines",
                name=labels[coin],
                line=dict(
                    color=colors[coin],
                    width=2
                )
            ),
            row=i,
            col=1
        )

        # Moving Average Line
        fig.add_trace(
            go.Scatter(
                x=coins[coin]["times"],
                y=coins[coin]["ma7"],
                mode="lines",
                name=f"{labels[coin]} MA7",
                line=dict(width=1)
            ),
            row=i,
            col=1
        )

    # --------------------------------------------------
    # Dashboard Styling
    #
    # Controls:
    # - title
    # - size
    # - theme
    # - legend
    # --------------------------------------------------
    fig.update_layout(
        title="Crypto Price Dashboard - Last 24 Hours",
        height=900,
        template="plotly_dark",
        showlegend=True
    )

    # --------------------------------------------------
    # Format Y Axis
    #
    # Example:
    #
    # $71,000
    #
    # instead of:
    #
    # 71000
    # --------------------------------------------------
    fig.update_yaxes(
        tickprefix="$",
        tickformat=",.0f"
    )

    # --------------------------------------------------
    # Export Dashboard
    #
    # Generates:
    #
    # dashboard.html
    #
    # which can be opened in any browser.
    # --------------------------------------------------
    fig.write_html("dashboard.html")

    print("Dashboard saved to dashboard.html")


# --------------------------------------------------
# Program Entry Point
#
# Tells Python where execution begins.
#
# When you run:
#
# python3 dashboard.py
#
# build_dashboard() gets executed.
# --------------------------------------------------
if __name__ == "__main__":
    build_dashboard()