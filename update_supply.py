import requests
import json
import os
from dotenv import load_dotenv

# 環境変数からAPIキー読み込み
load_dotenv()
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
TOKEN_MINT = "HJwToCxFFmtnYGZMQa7rZwHAMG2evdbdXAbbQr1Jpump"
INITIAL_SUPPLY = 1_000_000_000.0

if not HELIUS_API_KEY:
    raise Exception("❌ HELIUS_API_KEY is not set in .env")

# Helius APIで現在の供給量を取得
url = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
headers = {"Content-Type": "application/json"}
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getTokenSupply",
    "params": [TOKEN_MINT],
}

print("📡 Fetching current supply from Helius...")
response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()
data = response.json()

# 現在供給量とバーン量計算
current_supply = float(data["result"]["value"]["uiAmount"])
burned = round(INITIAL_SUPPLY - current_supply, 6)

# 割合ベースの再配分（current_supplyを100%とする）
ratios = {
    "Developer Lock": 0.10,
    "Operational Reserve": 0.15,
    "Marketing and Partnerships": 0.10,
    "Ecosystem Rewards": 0.10,
    "Community": 0.55
}

allocations = {}
total_allocated = 0

# 割合に応じて金額を計算（最後の項目で調整）
items = list(ratios.items())
for i, (name, ratio) in enumerate(items):
    if i < len(items) - 1:
        amount = round(current_supply * ratio, 6)
        allocations[name] = amount
        total_allocated += amount
    else:
        # 調整して誤差なしにする
        amount = round(current_supply - total_allocated, 6)
        allocations[name] = amount

# 結果をまとめる
result = {
    "mint": TOKEN_MINT,
    "initial_supply": INITIAL_SUPPLY,
    "current_supply": current_supply,
    "burned": burned,
    "allocations": allocations
}

# JSONファイル出力
with open("allocation_result.json", "w") as f:
    json.dump(result, f, indent=2)

print("✅ allocation_result.json has been created.")
