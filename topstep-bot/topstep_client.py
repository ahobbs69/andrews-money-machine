import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.topstepx.com/api"  # ProjectX / TopstepX Gateway base

USERNAME = os.getenv("TOPSTEP_USERNAME")
API_KEY = os.getenv("TOPSTEP_API_KEY")
ACCOUNT_ID = os.getenv("TOPSTEP_ACCOUNT_ID")

if not USERNAME:
    raise RuntimeError("TOPSTEP_USERNAME not set in environment (.env)")
if not API_KEY:
    raise RuntimeError("TOPSTEP_API_KEY not set in environment (.env)")
if not ACCOUNT_ID:
    raise RuntimeError("TOPSTEP_ACCOUNT_ID not set in environment (.env)")


class TopstepClient:
    """Client for ProjectX / TopstepX Gateway API.

    Auth flow (from docs):
    1. POST /Auth/loginKey with { userName, apiKey }
    2. Receive { token, success, errorCode, errorMessage }
    3. Use token as JWT for subsequent requests.
    """

    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.token = None
        self._authenticate()

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

    def _handle_response(self, resp):
        if not resp.ok:
            raise RuntimeError(f"TopstepX API error {resp.status_code}: {resp.text}")
        return resp.json()

    # NOTE: The following endpoints are placeholders; we'll adjust paths
    # once we see the concrete ProjectX docs for accounts/positions/orders.

    def get_account_info(self):
        """Fetch account info for ACCOUNT_ID.

        TODO: adjust path to match actual ProjectX Gateway route.
        """
        url = f"{self.base_url}/accounts/{ACCOUNT_ID}"
        resp = self.session.get(url)
        return self._handle_response(resp)

    def get_open_positions(self):
        url = f"{self.base_url}/accounts/{ACCOUNT_ID}/positions"
        resp = self.session.get(url)
        return self._handle_response(resp)

    def get_orders(self):
        url = f"{self.base_url}/accounts/{ACCOUNT_ID}/orders"
        resp = self.session.get(url)
        return self._handle_response(resp)

    def place_order(self, symbol, side, quantity, order_type="market", stop_loss=None, take_profit=None):
        """Place an order (schema to be aligned with actual ProjectX docs).

        side: 'buy' or 'sell'
        order_type: 'market' (for now)
        """
        url = f"{self.base_url}/accounts/{ACCOUNT_ID}/orders"
        payload = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "type": order_type,
        }

        if stop_loss is not None:
            payload["stop_loss"] = stop_loss
        if take_profit is not None:
            payload["take_profit"] = take_profit

        resp = self.session.post(url, json=payload)
        return self._handle_response(resp)

    def cancel_order(self, order_id):
        url = f"{self.base_url}/accounts/{ACCOUNT_ID}/orders/{order_id}"
        resp = self.session.delete(url)
        return self._handle_response(resp)
