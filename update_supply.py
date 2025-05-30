import requests
import json
import os
from dotenv import load_dotenv

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
    "params": [
        [TOKEN_MINT]  # ← 必ず2重リストにする
    ],
}

print("Request payload:", json.dumps(payload, indent=2))

response = requests.post(url, headers=headers, json=payload)

print("Response status code:", response.status_code)
print("Response content:", response.text)

if response.status_code != 200:
    raise Exception(f"❌ HTTP error: {response.status_code} - {response.text}")

data = response.json()

try:
    supply_info = data["result"]["value"]
    ui_amount = float(supply_info.get("uiAmount", 0))
    print("✅ Supply updated:", ui_amount)

except KeyError as e:
    raise RuntimeError(f"❌ 取得したレスポンス形式が予想と異なります。\nResponse: {json.dumps(data, indent=2)}") from e

with open("moj-supply.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("✅ Supply JSONを更新しました。")

