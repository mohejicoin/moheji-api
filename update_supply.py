import requests
import json
import os
from dotenv import load_dotenv

# .envから読み込み（ローカル用）
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
    "params": [TOKEN_MINT],  # ★ここは必ず配列（リスト）で
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
except KeyError as e:
    raise RuntimeError(
        f"❌ 取得したレスポンス形式が予想と異なります。\nResponse: {json.dumps(data, indent=2)}"
    ) from e

output_data = {
    "name": "moheji",
    "symbol": "MOJ",
    "decimals": 6,
    "total_supply": 1000000000,
    "circulating_supply": ui_amount,
    "burned_supply": 175506.628,
    "last_updated": "2025-05-29T00:00:00Z",
}

with open("moj-supply.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("✅ Supply JSONを更新しました。")

