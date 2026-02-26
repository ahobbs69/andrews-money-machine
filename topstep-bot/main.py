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

POLL_SECONDS = 10  # how often to check / generate signals


def log(msg: str):
    print(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}")


def main():
    client = TopstepClient()
    risk = RiskManager()
    strat = BreakoutStrategy(symbol=SYMBOL, base_size=1)

    log(f"Starting bot in MODE={MODE}, SYMBOL={SYMBOL}")

    while True:
        try:
            # 1) Pull account info (incl. realized PnL)
            account = client.get_account_info()
            # You'll need to adjust these keys based on actual TopstepX response
            realized_pnl = float(account.get("realized_pnl_today", 0.0))
            risk.update_realized_pnl(realized_pnl)

            if not risk.can_trade_today():
                log(f"Daily loss limit hit (PnL={realized_pnl}). No more trading today.")
                time.sleep(POLL_SECONDS)
                continue

            # 2) Pull market data (placeholder  depends on TopstepX API)
            # For now we'll stub this as an empty dict
            market_data = {}

            # 3) Strategy decides if there's a trade
            signal = strat.evaluate(market_data)

            if signal is None:
                log("No signal.")
                time.sleep(POLL_SECONDS)
                continue

            # 4) Risk checks on size
            if not risk.validate_order_size(signal.quantity):
                log(f"Signal rejected: size {signal.quantity} > MAX_CONTRACTS")
                time.sleep(POLL_SECONDS)
                continue

            log(f"Signal: {signal.side} {signal.quantity}x {SYMBOL} ({signal.reason})")

            if MODE == "paper":
                # Log only, no live orders
                log("MODE=paper  not sending real order.")
            else:
                # Live order
                resp = client.place_order(
                    symbol=SYMBOL,
                    side=signal.side,
                    quantity=signal.quantity,
                    order_type="market",
                )
                log(f"Order placed: {resp}")

        except Exception as e:
            log(f"Error in main loop: {e}")

        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
