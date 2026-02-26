from dataclasses import dataclass
from typing import Optional, Literal, List, Dict, Any

Side = Literal["buy", "sell"]


@dataclass
class Signal:
    side: Side
    quantity: int
    reason: str


class BreakoutStrategy:
    """Simple MES breakout strategy on recent bars.

    Idea (conservative for eval):
    - Use N bars lookback (e.g. last 30 1-minute bars).
    - Compute recent high/low of that window.
    - If price breaks above recent high by a small buffer → buy.
    - If price breaks below recent low by a small buffer → sell.
    - Only 1 signal per direction per session for now (handled at higher level).
    """

    def __init__(self, symbol: str, base_size: int = 1, lookback: int = 30, buffer_ticks: float = 1.0):
        self.symbol = symbol
        self.base_size = base_size
        self.lookback = lookback
        self.buffer_ticks = buffer_ticks

    def evaluate(self, bars: List[Dict[str, Any]]) -> Optional[Signal]:
        """Evaluate breakout on a list of bars.

        bars: list of dicts with keys t, o, h, l, c, v (as from History/retrieveBars)
        Returns a Signal or None.
        """
        if not bars or len(bars) < self.lookback + 1:
            return None

        # Ensure bars are sorted oldest → newest
        bars_sorted = sorted(bars, key=lambda b: b.get("t"))

        window = bars_sorted[-(self.lookback + 1):-1]
        last_bar = bars_sorted[-1]

        highs = [float(b.get("h", 0.0)) for b in window]
        lows = [float(b.get("l", 0.0)) for b in window]

        if not highs or not lows:
            return None

        recent_high = max(highs)
        recent_low = min(lows)
        last_close = float(last_bar.get("c", 0.0))

        if last_close == 0.0:
            return None

        # Simple breakout conditions with small buffer
        # NOTE: For MES tickSize = 0.25; buffer_ticks is in price units.
        if last_close > recent_high + self.buffer_ticks:
            return Signal(side="buy", quantity=self.base_size, reason=f"Breakout above recent high {recent_high:.2f} with close {last_close:.2f}")

        if last_close < recent_low - self.buffer_ticks:
            return Signal(side="sell", quantity=self.base_size, reason=f"Breakdown below recent low {recent_low:.2f} with close {last_close:.2f}")

        return None
