import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.topstepx.com/api"  # ProjectX / TopstepX Gateway base

USERNAME = os.getenv("TOPSTEP_USERNAME")
API_KEY = os.getenv("TOPSTEP_API_KEY")
# Optional: explicit account id; otherwise we'll discover via /Account/search
EXPLICIT_ACCOUNT_ID = os.getenv("TOPSTEP_ACCOUNT_ID")
# Target symbol we want to trade (can be MES, MNQ, M2K, etc.)
TARGET_SYMBOL_ID = os.getenv("TARGET_SYMBOL_ID", "F.US.MES")

if not USERNAME:
    raise RuntimeError("TOPSTEP_USERNAME not set in environment (.env)")
if not API_KEY:
    raise RuntimeError("TOPSTEP_API_KEY not set in environment (.env)")


class TopstepClient:
    """Client for ProjectX / TopstepX Gateway API.

    Handles:
    - Auth (loginKey + validate)
    - Account discovery (Account/search)
    - Contract discovery for a target symbol (Contract/available + search)
    - History bars (History/retrieveBars)
    - Orders (place/searchOpen/cancel)
    """

    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.token = None
        self.account_id = None
        self.contract_id = None  # contract we actually trade
        self._authenticate()
        self._discover_account()
        self._discover_contract()

    # --- Auth ---

    def _authenticate(self):
        """Authenticate with loginKey and store JWT token."""
        url = f"{self.base_url}/Auth/loginKey"
        payload = {
            "userName": USERNAME,
            "apiKey": API_KEY,
        }
        resp = self.session.post(url, json=payload, headers={
            "accept": "text/plain",
            "Content-Type": "application/json",
        })
        if not resp.ok:
            raise RuntimeError(f"Auth failed {resp.status_code}: {resp.text}")

        data = resp.json()
        if not data.get("success") or data.get("errorCode") not in (0, None):
            raise RuntimeError(f"Auth error: {data}")

        token = data.get("token")
        if not token:
            raise RuntimeError(f"Auth response missing token: {data}")

        self.token = token
        # Set Authorization header for future requests
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    def validate_token(self):
        """Validate current token (optional periodic check)."""
        url = f"{self.base_url}/Auth/validate"
        resp = self.session.post(url, json={})
        if not resp.ok:
            raise RuntimeError(f"Token validation failed {resp.status_code}: {resp.text}")
        return resp.json()

    # --- Accounts ---

    def _discover_account(self):
        """Find an active account to trade.

        Uses /Account/search with onlyActiveAccounts=true.
        If EXPLICIT_ACCOUNT_ID is set, prefer that id.
        """
        url = f"{self.base_url}/Account/search"
        payload = {"onlyActiveAccounts": True}
        resp = self.session.post(url, json=payload)
        data = self._handle_response(resp)

        if not data.get("success") or data.get("errorCode") not in (0, None):
            raise RuntimeError(f"Account search error: {data}")

        accounts = data.get("accounts") or []
        if not accounts:
            raise RuntimeError("No active accounts returned by /Account/search")

        chosen = None
        if EXPLICIT_ACCOUNT_ID is not None:
            try:
                target_id = int(EXPLICIT_ACCOUNT_ID)
            except ValueError:
                target_id = EXPLICIT_ACCOUNT_ID
            for acc in accounts:
                if acc.get("id") == target_id:
                    chosen = acc
                    break

        if chosen is None:
            chosen = accounts[0]

        self.account_id = chosen.get("id")
        if self.account_id is None:
            raise RuntimeError(f"Chosen account missing id: {chosen}")

    def get_account_info(self):
        """Return account info via /Account/search for our account_id."""
        url = f"{self.base_url}/Account/search"
        payload = {"onlyActiveAccounts": True}
        resp = self.session.post(url, json=payload)
        data = self._handle_response(resp)
        accounts = data.get("accounts") or []
        for acc in accounts:
            if acc.get("id") == self.account_id:
                return acc
        return None

    # --- Contracts ---

    def _discover_contract(self):
        """Find a tradable contract for TARGET_SYMBOL_ID.

        Tries /Contract/available first, then /Contract/search.
        If still nothing, falls back to the first active contract in available.
        """
        # 1) Try Contract/available
        url = f"{self.base_url}/Contract/available"
        payload = {"live": True}
        resp = self.session.post(url, json=payload)
        data = self._handle_response(resp)

        chosen_id = None
        if data.get("success") and data.get("errorCode") in (0, None):
            contracts = data.get("contracts") or []
            for c in contracts:
                if c.get("activeContract") and str(c.get("symbolId")) == TARGET_SYMBOL_ID:
                    chosen_id = c.get("id")
                    break

            # fallback: first active contract if target not found
            if not chosen_id and contracts:
                active_first = next((c for c in contracts if c.get("activeContract")), None)
                if active_first:
                    chosen_id = active_first.get("id")

        # 2) If still nothing, try Contract/search with searchText from TARGET_SYMBOL_ID
        if not chosen_id:
            # derive a short search text (e.g. MES from F.US.MES)
            search_text = TARGET_SYMBOL_ID.split(".")[-1]
            url = f"{self.base_url}/Contract/search"
            payload = {"live": True, "searchText": search_text}
            resp = self.session.post(url, json=payload)
            data = self._handle_response(resp)
            if data.get("success") and data.get("errorCode") in (0, None):
                contracts = data.get("contracts") or []
                for c in contracts:
                    if c.get("activeContract"):
                        chosen_id = c.get("id")
                        break

        if not chosen_id:
            raise RuntimeError("Could not find any tradable contract via available/search. Check TARGET_SYMBOL_ID or account permissions.")

        self.contract_id = chosen_id

    # --- History / Bars ---

    def get_recent_bars(self, limit: int = 50, unit: int = 2, unit_number: int = 1):
        """Retrieve recent bars for the chosen contract using History/retrieveBars.

        unit: 2 = minute bars
        unit_number: number of minutes per bar
        """
        if not self.contract_id:
            raise RuntimeError("contract_id not set")

        url = f"{self.base_url}/History/retrieveBars"

        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=4)

        payload = {
            "contractId": self.contract_id,
            "live": True,
            "startTime": start_time.isoformat().replace("+00:00", "Z"),
            "endTime": end_time.isoformat().replace("+00:00", "Z"),
            "unit": unit,
            "unitNumber": unit_number,
            "limit": limit,
            "includePartialBar": False,
        }

        resp = self.session.post(url, json=payload)
        data = self._handle_response(resp)

        if not data.get("success") or data.get("errorCode") not in (0, None):
            raise RuntimeError(f"History/retrieveBars error: {data}")

        return data.get("bars") or []

    # --- Orders ---

    def place_market_order_with_brackets(
        self,
        side: str,
        size: int,
        stop_ticks: int,
        take_profit_ticks: int,
        custom_tag: str | None = None,
    ):
        """Place a market order with stop/TP brackets on the chosen contract.

        side: 'buy' or 'sell'
        size: number of contracts
        """
        if not self.account_id or not self.contract_id:
            raise RuntimeError("Account or contract not initialized")

        side_enum = 0 if side == "buy" else 1  # 0=Bid (buy), 1=Ask (sell)

        url = f"{self.base_url}/Order/place"
        payload = {
            "accountId": self.account_id,
            "contractId": self.contract_id,
            "type": 2,  # Market
            "side": side_enum,
            "size": size,
            "limitPrice": None,
            "stopPrice": None,
            "trailPrice": None,
            "customTag": custom_tag,
            "stopLossBracket": {
                "ticks": stop_ticks,
                "type": 1,  # Limit (enum per docs)
            },
            "takeProfitBracket": {
                "ticks": take_profit_ticks,
                "type": 1,  # Limit
            },
        }

        resp = self.session.post(url, json=payload)
        data = self._handle_response(resp)
        if not data.get("success") or data.get("errorCode") not in (0, None):
            raise RuntimeError(f"Order/place error: {data}")
        return data

    def search_open_orders(self):
        if not self.account_id:
            raise RuntimeError("Account id not set")
        url = f"{self.base_url}/Order/searchOpen"
        payload = {"accountId": self.account_id}
        resp = self.session.post(url, json=payload)
        data = self._handle_response(resp)
        if not data.get("success") or data.get("errorCode") not in (0, None):
            raise RuntimeError(f"Order/searchOpen error: {data}")
        return data.get("orders") or []

    def cancel_order(self, order_id: int):
        if not self.account_id:
            raise RuntimeError("Account id not set")
        url = f"{self.base_url}/Order/cancel"
        payload = {"accountId": self.account_id, "orderId": order_id}
        resp = self.session.post(url, json=payload)
        data = self._handle_response(resp)
        if not data.get("success") or data.get("errorCode") not in (0, None):
            raise RuntimeError(f"Order/cancel error: {data}")
        return data

    # --- Helpers ---

    def _handle_response(self, resp: requests.Response):
        if not resp.ok:
            raise RuntimeError(f"TopstepX API error {resp.status_code}: {resp.text}")
        return resp.json()
