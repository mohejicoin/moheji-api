import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
TOKEN_MINT = "HJwToCxFFmtnYGZMQa7rZwHAMG2evdbdXAbbQr1Jpump"

if not HELIUS_API_KEY:
    raise Exception("❌ HELIUS_API_KEY is not set.")

url = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
headers = {"Content-Type": "application/json"}
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getTokenSupply",
    "params": [TOKEN_MINT],
}

print("📡 Getting supply from Helius...")
response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()
data = response.json()
supply = data["result"]["value"]["uiAmount"]

# Save to moj-supply.json
with open("moj-supply.json", "w") as f:
    json.dump({"mint": TOKEN_MINT, "supply": supply}, f, indent=2)

print(f"✅ Supply: {supply}")

# Allocation breakdown
allocations = {
    "Developer Lock": round(supply * 0.10, 6),
    "Operational Reserve": round(supply * 0.15, 6),
    "Marketing and Partnerships": round(supply * 0.10, 6),
    "Ecosystem Rewards": round(supply * 0.10, 6),
    "Burn Slot": round(supply * 0.05, 6),
    "Community": round(supply * 0.50, 6),
}

with open("allocation_result.json", "w") as f:
    json.dump({"total_supply": supply, "allocations": allocations}, f, indent=2)

print("✅ allocation_result.json has been created.")
