import requests
import json
import os
from dotenv import load_dotenv

# 環境変数を読み込む（HELIUS_API_KEY）
load_dotenv()
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
TOKEN_MINT = "HJwToCxFFmtnYGZMQa7rZwHAMG2evdbdXAbbQr1Jpump"

# エラーチェック
if not HELIUS_API_KEY:
    raise Exception("❌ HELIUS_API_KEY is not set.")

# Helius API で現在供給量を取得
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

# ✅ 初期供給量（固定）
initial_supply = 1_000_000_000  # 10億MOJ

# 🔥 現在バーンされた量
burned_amount = round(initial_supply - current_supply, 6)

# 📊 初期供給量に基づく固定アロケーション
allocations = {
    "Developer Lock": round(initial_supply * 0.10, 6),
    "Operational Reserve": round(initial_supply * 0.15, 6),
    "Marketing and Partnerships": round(initial_supply * 0.10, 6),
    "Ecosystem Rewards": round(initial_supply * 0.10, 6),
    "Burn Slot": burned_amount,
    "Community": round(initial_supply * 0.50, 6),
}

# 📝 JSONファイルに保存
with open("moj-supply.json", "w") as f:
    json.dump({
        "mint": TOKEN_MINT,
        "current_supply": current_supply,
        "initial_supply": initial_supply,
        "burned": burned_amount
    }, f, indent=2)

with open("allocation_result.json", "w") as f:
    json.dump({
        "initial_supply": initial_supply,
        "current_supply": current_supply,
        "burned": burned_amount,
        "allocations": allocations
    }, f, indent=2)

# ✅ 完了メッセージ
print(f"✅ Current supply: {current_supply}")
print("✅ allocation_result.json has been created.")
