import os
import httpx

class DynexAPIClient:
    """HTTP API client for Dynex advanced workflows."""
    def __init__(self, endpoint=None, api_key=None, api_secret=None):
        self.endpoint = endpoint or os.getenv("DYNEX_API_ENDPOINT")
        self.api_key = api_key or os.getenv("DYNEX_API_KEY")
        self.api_secret = api_secret or os.getenv("DYNEX_API_SECRET")
        self.session = httpx.AsyncClient()

    async def post(self, path, data=None):
        url = f"{self.endpoint.rstrip('/')}/{path.lstrip('/')}"
        headers = {
            "X-API-KEY": self.api_key,
            "X-API-SECRET": self.api_secret,
            "Content-Type": "application/json"
        }
        resp = await self.session.post(url, json=data, headers=headers)
        resp.raise_for_status()
        return resp.json()

    async def get(self, path, params=None):
        url = f"{self.endpoint.rstrip('/')}/{path.lstrip('/')}"
        headers = {
            "X-API-KEY": self.api_key,
            "X-API-SECRET": self.api_secret,
        }
        resp = await self.session.get(url, params=params, headers=headers)
        resp.raise_for_status()
        return resp.json()
