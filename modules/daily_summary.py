SUMMARY_THRESHOLD = 100000000  # ₹10 Crore


def build_section(df, title):

    if df.empty:
        return ""

    message = f"{title}\n"

    for _, row in df.iterrows():

        value_cr = row["total_value"] / 10000000
        players = row["players"]

        player_text = "Player" if players == 1 else "Players"

        message += (
            f"{row['symbol']} — ₹{value_cr:.2f} Cr "
            f"({player_text}: {players})\n"
        )

    message += "\n"

    return message


def format_daily_summary(df):

    if df.empty:
        return None

    date = df["date"].iloc[0]

    message = "📊 Institutional Daily Summary\n\n"
    message += f"Date: {date}\n\n"

    # ---- BULK BUYERS ----
    bulk_buy = df[
        (df["deal_type"] == "BULK DEAL") &
        (df["buySell"] == "BUY")
    ]

    bulk_buy = (
        bulk_buy.groupby(["symbol", "date"])
        .agg(
            total_value=("total_value", "sum"),
            players=("client", "nunique")
        )
        .reset_index()
    )

    bulk_buy = bulk_buy[bulk_buy["total_value"] >= SUMMARY_THRESHOLD]

    # ---- BULK SELLERS ----
    bulk_sell = df[
        (df["deal_type"] == "BULK DEAL") &
        (df["buySell"] == "SELL")
    ]

    bulk_sell = (
        bulk_sell.groupby(["symbol", "date"])
        .agg(
            total_value=("total_value", "sum"),
            players=("client", "nunique")
        )
        .reset_index()
    )

    bulk_sell = bulk_sell[bulk_sell["total_value"] >= SUMMARY_THRESHOLD]

    # ---- BLOCK BUYERS ----
    block_buy = df[
        (df["deal_type"] == "BLOCK DEAL") &
        (df["buySell"] == "BUY")
    ]

    block_buy = (
        block_buy.groupby(["symbol", "date"])
        .agg(
            total_value=("total_value", "sum"),
            players=("client", "nunique")
        )
        .reset_index()
    )

    # ---- BLOCK SELLERS ----
    block_sell = df[
        (df["deal_type"] == "BLOCK DEAL") &
        (df["buySell"] == "SELL")
    ]

    block_sell = (
        block_sell.groupby(["symbol", "date"])
        .agg(
            total_value=("total_value", "sum"),
            players=("client", "nunique")
        )
        .reset_index()
    )

    message += build_section(bulk_buy, "BULK DEAL BUYERS")
    message += build_section(bulk_sell, "BULK DEAL SELLERS")
    message += build_section(block_buy, "BLOCK DEAL BUYERS")
    message += build_section(block_sell, "BLOCK DEAL SELLERS")

    return message