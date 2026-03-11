TRANSFER_THRESHOLD = 100000000  # ₹10 Cr


def format_block_transfer_message(df):

    if df.empty:
        return None

    date = df["date"].iloc[0]

    message = "📦 Block Deal Transfers\n\n"
    message += f"Date: {date}\n\n"

    symbols = df["symbol"].unique()

    found = False

    for symbol in symbols:

        symbol_df = df[df["symbol"] == symbol]

        total_value = symbol_df["total_value"].sum()

        if total_value < TRANSFER_THRESHOLD:
            continue

        buy_row = symbol_df[symbol_df["buySell"] == "BUY"]
        sell_row = symbol_df[symbol_df["buySell"] == "SELL"]

        if buy_row.empty or sell_row.empty:
            continue

        buyer = buy_row.iloc[0]["client"]
        seller = sell_row.iloc[0]["client"]

        price = buy_row.iloc[0]["avg_price"]

        value_cr = total_value / 10000000

        message += (
            f"{symbol} — ₹{value_cr:.2f} Cr — Price ₹{price:.2f}\n"
            f"Buyer: {buyer}\n"
            f"Seller: {seller}\n\n"
        )

        found = True

    if not found:
        message += "No block deal transfers detected today."

    return message