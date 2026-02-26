from dataclasses import dataclass
from typing import Optional, Literal

Side = Literal["buy", "sell"]


@dataclass
class Signal:
    side: Side
    quantity: int
    reason: str


class BreakoutStrategy:
    """\
    Very simple placeholder:
    - In real-time, we'd compute session range, recent highs/lows, etc.
    - For now, we will stub out a decision function.
    """

    def __init__(self, symbol: str, base_size: int = 1):
        self.symbol = symbol
        self.base_size = base_size

    def evaluate(self, market_data: dict) -> Optional[Signal]:
        """\
        market_data: dict with latest prices, range, etc.
        For now, this returns None (no trade).
        We'll fill this in once we decide exact breakout logic.
        """
        # TODO: implement breakout logic once we know what data TopstepX provides
        return None
