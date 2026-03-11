import pandas as pd

BULK_THRESHOLD = 100000000  # ₹10 Cr


def detect_flow(df, deal_type):
    """
    Detect accumulation and distribution for a given deal type
    """

    accumulation = []
    distribution = []

    # Separate buy and sell
    buy_df = df[df["buySell"] == "BUY"]
    sell_df = df[df["buySell"] == "SELL"]

    # ---- ACCUMULATION ----
    buy_group = (
        buy_df.groupby(["symbol", "date"])
        .agg(
            buyers=("client", "nunique"),
            total_value=("total_value", "sum"),
            min_price=("avg_price", "min"),
            max_price=("avg_price", "max"),
        )
        .reset_index()
    )

    for _, row in buy_group.iterrows():

        buyers = row["buyers"]
        value = row["total_value"]

        if deal_type == "BULK DEAL":
            if buyers >= 2 and value >= BULK_THRESHOLD:
                accumulation.append(row)

    # ---- DISTRIBUTION ----
    sell_group = (
        sell_df.groupby(["symbol", "date"])
        .agg(
            sellers=("client", "nunique"),
            total_value=("total_value", "sum"),
            min_price=("avg_price", "min"),
            max_price=("avg_price", "max"),
        )
        .reset_index()
    )

    for _, row in sell_group.iterrows():

        sellers = row["sellers"]
        value = row["total_value"]

        if deal_type == "BULK DEAL":
            if sellers >= 2 and value >= BULK_THRESHOLD:
                distribution.append(row)

    return accumulation, distribution


def format_flow_message(df, deal_type):
    """
    Build Telegram message for accumulation + distribution
    """

    if df.empty:
        return None

    date = df["date"].iloc[0]

    accumulation, distribution = detect_flow(df, deal_type)

    message = f"🔥 Institutional Flow Alert\n\n"
    message += f"Date: {date}\n"
    message += f"Deal Type: {deal_type}\n\n"

    # Accumulation
    if accumulation:

        message += "Accumulation\n"

        for row in accumulation:

            price_range = (
                f"₹{row['min_price']:.2f}"
                if row["min_price"] == row["max_price"]
                else f"₹{row['min_price']:.2f}–₹{row['max_price']:.2f}"
            )

            value_cr = row["total_value"] / 10000000

            message += (
                f"{row['symbol']} — Buyers: {row['buyers']} "
                f"— ₹{value_cr:.2f} Cr — Price {price_range}\n"
            )

        message += "\n"

    # Distribution
    if distribution:

        message += "Distribution\n"

        for row in distribution:

            price_range = (
                f"₹{row['min_price']:.2f}"
                if row["min_price"] == row["max_price"]
                else f"₹{row['min_price']:.2f}–₹{row['max_price']:.2f}"
            )

            value_cr = row["total_value"] / 10000000

            message += (
                f"{row['symbol']} — Sellers: {row['sellers']} "
                f"— ₹{value_cr:.2f} Cr — Price {price_range}\n"
            )

    # If nothing detected
    if not accumulation and not distribution:

        message += "No accumulation or distribution detected today."

    return message