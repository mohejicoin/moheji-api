import requests
import json
import os
from dotenv import load_dotenv

# .env 読み込み
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
        TOKEN_MINT
    ],
}

print("Request payload:", json.dumps(payload, indent=2))

# API リクエスト送信
try:
    response = requests.post(url, headers=headers, json=payload)
    print("Response status code:", response.status_code)
    print("Response content:", response.text)
except requests.RequestException as e:
    raise RuntimeError(f"❌ リクエストエラー: {e}")

if response.status_code != 200:
    raise Exception(f"❌ HTTP error: {response.status_code} - {response.text}")

# レスポンス処理
try:
    data = response.json()

    result = data.get("result")
    if not result or "value" not in result:
        raise KeyError("❌ 'result.value' がレスポンスに存在しません。")

    supply_info = result["value"]
    ui_amount = float(supply_info.get("uiAmount", 0))
    print("✅ Supply updated:", ui_amount)

    output_data = {
        "mint": TOKEN_MINT,
        "supply": ui_amount
    }

    try:
        with open("moj-supply.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print("✅ Supply JSONを更新しました。")
    except Exception as e:
        print("❌ JSON保存中にエラーが発生しました:", e)

except (KeyError, ValueError, json.JSONDecodeError) as e:
    raise RuntimeError(f"❌ レスポンスの解析中にエラーが発生しました。\nResponse: {json.dumps(data, indent=2)}") from e

