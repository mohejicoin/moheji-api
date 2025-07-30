import requests
import json
import os
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
TOKEN_MINT = "HJwToCxFFmtnYGZMQa7rZwHAMG2evdbdXAbbQr1Jpump"

# Initial supply amount（1B）
INITIAL_SUPPLY = 1_000_000_000.0

if not HELIUS_API_KEY:
    raise Exception("❌ HELIUS_API_KEY is not set.")

# Get supply from Helius API
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
current_supply = data["result"]["value"]["uiAmount"]
burned = round(INITIAL_SUPPLY - current_supply, 6)

# Percentage setting (recalculated as 100% excluding burned)
ratios = {
    "Developer Lock": 0.0025,
    "Operational Reserve": 0.0025,
    "Marketing and Partnerships": 0.0025,
    "Ecosystem Rewards": 0.0025,
    "Community": 0.99 # All the rest
}

# Check that the percentages sum to 1.0
assert round(sum(ratios.values()), 6) == 1.0, "❌ The percentages do not add up to 100%"

# Recalculate allocation based on current_supply
allocations = {
    k: round(current_supply * v, 6) for k, v in ratios.items()
}

# Summarizing the results
result = {
    "mint": TOKEN_MINT,
    "initial_supply": INITIAL_SUPPLY,
    "current_supply": current_supply,
    "burned": burned,
    "allocations": allocations
}

# Export JSON (new file name)
with open("moj-final-allocation.json", "w") as f:
    json.dump(result, f, indent=2)

print("✅ moj-final-allocation.json has been created.")
