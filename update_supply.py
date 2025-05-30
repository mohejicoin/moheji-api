import requests
import json
import os
from dotenv import load_dotenv

# ローカル環境なら .env を読み込み
if os.path.exists(".env"):
    load_dotenv()

HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
if not HELIUS_API_KEY:
    raise Exception("❌ HELIUS_API_KEY is not set.")

TOKEN_MINT = "HJwToCxFFmtnYGZMQa7rZwHAMG2evdbdXAbbQr1Jpump"
url = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
headers = {"Content-Type": "application/json"}

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getTokenSupply",
    "params": {
        "mint": TOKEN_MINT
    }
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code != 200:
    raise Exception(f"❌ HTTP error: {response.status_code} - {response.text}")

data = response.json()

if "result" in data and "value" in data["result"]:
    supply_info = data["result"]["value"]
    ui_amount = float(supply_info.get("uiAmount", 0))

    with open("moj-supply.json", "w") as f:
        json.dump({"total_supply": ui_amount}, f, indent=2)

    print("✅ Supply updated:", ui_amount)
else:
    raise Exception("❌ Unexpected response format:\n" + json.dumps(data, indent=2))
