import requests
import json
from datetime import datetime
import os

TOKEN_ADDRESS = "HJwToCxFFmtnYGZMQa7rZwHAMG2evdbdXAbbQr1Jpump"
api_key = os.getenv("HELIUS_API_KEY")

url = f"https://api.helius.xyz/v0/token-metadata?api-key={api_key}"

body = {
    "mintAccounts": [TOKEN_ADDRESS]
}

response = requests.post(url, json=body)
response.raise_for_status()  # エラーがあれば例外発生
data = response.json()

decimals = int(data[0]["decimals"])
raw_supply = int(data[0]["supply"])
supply = raw_supply / (10 ** decimals)

output = {
    "token": "moheji",
    "symbol": "MOJ",
    "supply": supply,
    "last_updated": datetime.utcnow().isoformat() + "Z"
}

with open("moj-supply.json", "w") as f:
    json.dump(output, f, indent=2)

print("✅ Updated moj-supply.json")


