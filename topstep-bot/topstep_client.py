import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.topstepx.com/api"  # ProjectX / TopstepX Gateway base

USERNAME = os.getenv("TOPSTEP_USERNAME")
API_KEY = os.getenv("TOPSTEP_API_KEY")
# Optional: explicit account id; otherwise we'll discover via /Account/search
EXPLICIT_ACCOUNT_ID = os.getenv("TOPSTEP_ACCOUNT_ID")

if not USERNAME:
    raise RuntimeError("TOPSTEP_USERNAME not set in environment (.env)")
if not API_KEY:
    raise RuntimeError("TOPSTEP_API_KEY not set in environment (.env)")


class TopstepClient:
    """Client for ProjectX / TopstepX Gateway API.

    Auth flow:
    1) POST /Auth/loginKey with { userName, apiKey }
    2) Store token from response
    3) Use Bearer token for all subsequent requests

    Account discovery:
    - POST /Account/search with { onlyActiveAccounts: true }
    - Pick an account (optionally matching EXPLICIT_ACCOUNT_ID)
    """

    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.token = None
        self.account_id = None
        self._authenticate()
        self._discover_account()

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
            # try to match integer id
            try:
                target_id = int(EXPLICIT_ACCOUNT_ID)
            except ValueError:
                target_id = EXPLICIT_ACCOUNT_ID
            for acc in accounts:
                if acc.get("id") == target_id:
                    chosen = acc
                    break

        if chosen is None:
            # default to first active account
            chosen = accounts[0]

        self.account_id = chosen.get("id")
        if self.account_id is None:
            raise RuntimeError(f"Chosen account missing id: {chosen}")

    def get_account_info(self):
        """Return the cached account info from last /Account/search call.

        For now, simply re-call search and pick our account again.
        Later we can switch to a dedicated account details endpoint if needed.
        """
        url = f"{self.base_url}/Account/search"
        payload = {"onlyActiveAccounts": True}
        resp = self.session.post(url, json=payload)
        data = self._handle_response(resp)
        accounts = data.get("accounts") or []
        for acc in accounts:
            if acc.get("id") == self.account_id:
                return acc
        return None

    # --- Contracts & Orders (to be expanded) ---

    def _handle_response(self, resp):
        if not resp.ok:
            raise RuntimeError(f"TopstepX API error {resp.status_code}: {resp.text}")
        return resp.json()

    # TODO: add methods for /Contract/available and /Order/place once we
    # know the exact contractId for MES and any side/type enum mappings.
