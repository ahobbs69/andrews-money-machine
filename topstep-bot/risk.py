import os
from dotenv import load_dotenv

load_dotenv()

MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", "250"))
MAX_CONTRACTS = int(os.getenv("MAX_CONTRACTS", "3"))


class RiskManager:
    def __init__(self):
        self.realized_pnl_today = 0.0

    def update_realized_pnl(self, realized_pnl):
        """Call this with the latest realized PnL for today."""
        self.realized_pnl_today = realized_pnl

    def can_trade_today(self):
        """Check if we are still within daily loss limit."""
        if self.realized_pnl_today <= -MAX_DAILY_LOSS:
            return False
        return True

    def validate_order_size(self, quantity):
        """Ensure we don't exceed max contracts."""
        if quantity > MAX_CONTRACTS:
            return False
        return True
