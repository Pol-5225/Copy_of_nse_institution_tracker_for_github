import pandas as pd
TRADE_THRESHOLD = 100000000  # ₹10 Crore


def filter_large_trades(df):
    """
    Filter trades where:
    1. Trade value > ₹10 Crore
    OR
    2. Client belongs to our institution keyword list
    """

    filtered = df[
        (df["total_value"] > TRADE_THRESHOLD) |
        (df["institution"].notna())
    ]

    return filtered


def format_alerts(df):
    """
    Convert filtered trades into readable alert messages
    """

    alerts = []

    for _, row in df.iterrows():

        # if institution detected use that, otherwise show client name
        name = row["institution"] if pd.notna(row["institution"]) else row["client"]

        message = (
            f"🚨 Institutional Activity Detected\n\n"
            f"Date: {row['date']}\n"
            f"Deal Type: {row['deal_type']}\n"
            f"Stock: {row['symbol']}\n"
            f"Client: {name}\n"
            f"Side: {row['buySell']}\n"
            f"Quantity: {int(row['total_quantity'])}\n"
            f"Average Price: ₹{round(row['avg_price'], 2)}\n"
            f"Trade Value: ₹{round(row['total_value']/10000000, 2)} Cr"
        )

        alerts.append(message)

    return alerts