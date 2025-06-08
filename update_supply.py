import requests
import json
import os
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
TOKEN_MINT = "HJwToCxFFmtnYGZMQa7rZwHAMG2evdbdXAbbQr1Jpump"

# 初期供給量（バーン前の総供給量）
INITIAL_SUPPLY = 1_000_000_000.0

if not HELIUS_API_KEY:
    raise Exception("❌ HELIUS_API_KEY is not set.")

# Helius APIのエンドポイントとヘッダー
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

# バーン量を計算
burned = round(INITIAL_SUPPLY - current_supply, 6)

# 固定配分計算（初期供給量ベース）
allocations = {
    "Developer Lock": round(INITIAL_SUPPLY * 0.10, 6),
    "Operational Reserve": round(INITIAL_SUPPLY * 0.10, 6),
    "Marketing and Partnerships": round(INITIAL_SUPPLY * 0.10, 6),
    "Ecosystem Rewards": round(INITIAL_SUPPLY * 0.10, 6),
    "Community": round(INITIAL_SUPPLY * 0.59, 6),
    "Burn Slot": burned,  # 実際のバーン量
}

# 結果を辞書でまとめる
result = {
    "mint": TOKEN_MINT,
    "initial_supply": INITIAL_SUPPLY,
    "current_supply": current_supply,
    "burned": burned,
    "allocations": allocations,
}

# JSONファイルに書き込み
with open("moj-final-allocation.json", "w") as f:
    json.dump(result, f, indent=2)

print("✅ moj-final-allocation.json has been created.")
