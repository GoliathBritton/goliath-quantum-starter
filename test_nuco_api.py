import httpx
import os

api_key = "ScSL33hX9EGPlUniqabdT6dYeHrc1gFl9xeWulSYleZhIGZdWFubb8Rd8LaC9GXxJweK61CpZlrKANq5HLr6Txry0KPOEd59csltQ0EIuLMmW2N1KkOV8szEX8mni1gnVEBbAdDZbnOruwlYr5eAEJpreOHNi22TTLBzmyE9OygCxcxxKDslbylXCCUaNgRT90pH8x64qwf2kPuNvNTUvPn2aHQ"  # Updated with provided API key
headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
base_url = "https://app.nuco.cloud/api"  # Testing /api without v1
client = httpx.Client(http2=True, follow_redirects=True)
# Test auth/available servers (mock response based on API desc)
response = client.get(f"{base_url}/v1/backends", headers=headers)
print(response.status_code)  # Expect 200 for valid key
print(response.text)  # Print raw response for debugging