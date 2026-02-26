import os
import time
from datetime import datetime
from dotenv import load_dotenv

from topstep_client import TopstepClient
from risk import RiskManager
from strategy import BreakoutStrategy

load_dotenv()

SYMBOL = os.getenv("SYMBOL", "MES")
MODE = os.getenv("MODE", "paper")  # 'paper' or 'live'

POLL_SECONDS = 30  # how often to check / generate signals


def log(msg: str):
    print(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}")


def main():
    client = TopstepClient()
    risk = RiskManager()
    # 1 contract base size for MES for now
    strat = BreakoutStrategy(symbol=SYMBOL, base_size=1, lookback=30, buffer_ticks=0.5)

    log(f"Starting bot in MODE={MODE}, SYMBOL={SYMBOL}")
    log("Initialized Topstep client, account, and MES contract.")

    while True:
        try:
            # 1) Account info – we currently just fetch it to confirm canTrade
            account = client.get_account_info()
            if not account:
                log("No account info returned; skipping loop.")
                time.sleep(POLL_SECONDS)
                continue

            can_trade = bool(account.get("canTrade", False))
            balance = account.get("balance")
            log(f"Account {account.get('name')} (id={account.get('id')}) balance={balance}, canTrade={can_trade}")

            if not can_trade:
                log("Account not tradable (canTrade=false). Skipping.")
                time.sleep(POLL_SECONDS)
                continue

            # NOTE: We don't yet have realized PnL field from API; for now,
            # RiskManager uses its default (0). We'll tighten this once we
            # wire in PnL via Order/search or a dedicated endpoint.

            if not risk.can_trade_today():
                log("Daily loss limit flag triggered. No more trading today.")
                time.sleep(POLL_SECONDS)
                continue

            # 2) Fetch recent MES bars
            try:
                bars = client.get_recent_bars(limit=60, unit=2, unit_number=1)
            except Exception as e:
                log(f"Error fetching bars: {e}")
                time.sleep(POLL_SECONDS)
                continue

            if not bars:
                log("No bars returned; skipping.")
                time.sleep(POLL_SECONDS)
                continue

            # 3) Strategy decides if there's a trade
            signal = strat.evaluate(bars)

            if signal is None:
                log("No signal.")
                time.sleep(POLL_SECONDS)
                continue

            # 4) Risk checks on size
            if not risk.validate_order_size(signal.quantity):
                log(f"Signal rejected: size {signal.quantity} > MAX_CONTRACTS")
                time.sleep(POLL_SECONDS)
                continue

            log(f"Signal: {signal.side.upper()} {signal.quantity}x {SYMBOL} ({signal.reason})")

            if MODE == "paper":
                # Log only, no live orders
                log("MODE=paper → not sending real order. This is a dry-run signal.")
            else:
                # Live order: place market order with conservative brackets
                # For MES, 10 ticks stop, 20 ticks TP as a starting point
                try:
                    resp = client.place_market_order_with_brackets(
                        side=signal.side,
                        size=signal.quantity,
                        stop_ticks=10,
                        take_profit_ticks=20,
                        custom_tag=f"ClydeMES-{datetime.utcnow().isoformat(timespec='seconds')}",
                    )
                    log(f"Order placed: {resp}")
                except Exception as e:
                    log(f"Error placing order: {e}")

        except Exception as e:
            log(f"Error in main loop: {e}")

        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
