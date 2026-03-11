import pandas as pd
from pathlib import Path
from modules.institution_detector import detect_institution

DATA_FOLDER = Path("data")


def prepare_dataframe(df):
    """
    Prepare dataframe for analysis
    """

    # clean column names
    df.columns = df.columns.str.strip().str.replace("\xa0", " ")

    # rename NSE columns safely
    column_map = {
        "Date": "date",
        "Symbol": "symbol",
        "Client Name": "client",
        "Buy/Sell": "buySell",
        "Quantity Traded": "qty",
        "Trade Price / Wght. Avg. Price": "price"
    }

    df = df.rename(columns=column_map)

    # convert numeric fields
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # calculate trade value
    df["trade_value"] = df["qty"] * df["price"]

    # detect institution
    df["institution"] = df["client"].apply(detect_institution)

    return df


def aggregate_trades(df):
    """
    Aggregate trades by:
    stock + client + institution + buy/sell
    """

    grouped = (
        df.groupby(
            ["symbol", "client", "institution", "buySell", "deal_type"],
            dropna=False
        )
        .agg(
            total_quantity=("qty", "sum"),
            avg_price=("price", "mean"),
            total_value=("trade_value", "sum"),
            date=("date", "first")
        )
        .reset_index()
    )

    return grouped