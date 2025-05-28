import requests
import json
import os
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

# 環境変数からAPIキー取得
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
if not HELIUS_API_KEY:
    raise Exception("❌ HELIUS_API_KEY is not set in the .env file.")

# MOJトークンのMintアドレス
TOKEN_MINT = "HJwToCxFFmtnYGZMQa7rZwHAMG2evdbdXAbbQr1Jpump"

# Helius RPC エンドポイント
url = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
headers = {"Content-Type": "application/json"}

# getTokenSupplyリクエストペイロード
payload = {
    "jsonrpc": "2.0",
    "id": "get-token-supply",
    "method": "getTokenSupply",
    "params": [TOKEN_MINT],
}

# リクエスト送信
response = requests.post(url, headers=headers, json=payload)
data = response.json()

# レスポンス処理
if "result" in data and "value" in data["result"]:
    supply_info = data["result"]["value"]
    decimals = int(supply_info.get("decimals", 6))
    ui_amount = float(supply_info.get("uiAmount", 0))

    # JSONファイルに保存
    with open("moj-supply.json", "w") as f:
        json.dump({
            "total_supply": round(ui_amount, decimals)
        }, f, indent=2)

    print("✅ Supply updated:", ui_amount)

else:
    raise Exception("❌ Unexpected response format:\n" + json.dumps(data, indent=2))
