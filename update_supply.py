import requests
import json
import os
from dotenv import load_dotenv

# ローカル実行用に .env から環境変数を読み込む
load_dotenv()

# GitHub Actions でも環境変数 HELIUS_API_KEY を取得
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
    "params": [TOKEN_MINT],
}

print("📡 Sending request to Helius RPC...")

try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    supply_value = data.get("result", {}).get("value", {}).get("uiAmount")
    if supply_value is None:
        raise KeyError("❌ 'uiAmount' not found in response.")
    supply = float(supply_value)
    print(f"✅ Current Supply: {supply}")

    # JSONファイルに出力
    output_data = {
        "mint": TOKEN_MINT,
        "supply": supply
    }
    with open("moj-supply.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print("✅ moj-supply.json を更新しました。")

except requests.RequestException as e:
    print(f"❌ Request error: {e}")
    exit(1)
except (KeyError, ValueError, json.JSONDecodeError) as e:
    print(f"❌ Response parsing error: {e}\nResponse content: {response.text}")
    exit(1)

