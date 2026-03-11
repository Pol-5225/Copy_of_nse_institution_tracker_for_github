import pandas as pd

from modules.daily_summary import format_daily_summary
from modules.block_transfer_detector import format_block_transfer_message
from modules.flow_detector import format_flow_message
from modules.downloader import download_bulk_deals, download_block_deals
from modules.parser import prepare_dataframe, aggregate_trades
from modules.alert_engine import filter_large_trades, format_alerts
from telegram.telegram_bot import send_message

def run_pipeline():

    # Step 1: Download NSE data
    download_bulk_deals()
    download_block_deals()

    # Step 2: Load downloaded data
    # Step 2: Load downloaded data
    bulk_df = pd.read_csv("data/bulk_deals.csv")
    bulk_df["deal_type"] = "BULK DEAL"

    block_df = pd.read_csv("data/block_deals.csv")
    block_df["deal_type"] = "BLOCK DEAL"

    # Step 4: Prepare data
    bulk_df = prepare_dataframe(bulk_df)
    block_df = prepare_dataframe(block_df)

    # Step 5: Aggregate trades
    bulk_agg = aggregate_trades(bulk_df)
    block_agg = aggregate_trades(block_df)

    # Step 6: Combine both datasets
    combined = pd.concat([bulk_agg, block_agg])

    # ---- BULK FLOW DETECTION ----
    bulk_flow_msg = format_flow_message(bulk_agg, "BULK DEAL")

    if bulk_flow_msg:
        send_message(bulk_flow_msg)

    # ---- BLOCK DEAL TRANSFERS ----
    block_transfer_msg = format_block_transfer_message(block_agg)

    if block_transfer_msg:
        send_message(block_transfer_msg)

    # Step 7: Filter large trades
    large_trades = filter_large_trades(combined)

    # Step 8: Format alerts
    alerts = format_alerts(large_trades)

    # Step 9: Send alerts to Telegram
    for alert in alerts:
        send_message(alert)

    # ---- DAILY SUMMARY ----
    summary_msg = format_daily_summary(combined)

    if summary_msg:
        send_message(summary_msg)

if __name__ == "__main__":
    run_pipeline()