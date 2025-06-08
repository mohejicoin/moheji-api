import requests
import json
import os
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
TOKEN_MINT = "HJwToCxFFmtnYGZMQa7rZwHAMG2evdbdXAbbQr1Jpump"

# 初期供給量（1B）
INITIAL_SUPPLY = 1_000_000_000.0

if not HELIUS_API_KEY:
    raise Exception("❌ HELIUS_API_KEY is not set.")

# Helius APIから供給量取得
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

# 割合設定（burnedを除いた100%として再計算）
ratios = {
    "Developer Lock": 0.10,
    "Operational Reserve": 0.15,
    "Marketing and Partnerships": 0.10,
    "Ecosystem Rewards": 0.10,
    "Community": 0.55  # 残りすべて
}

# 割合の合計が1.0であることを確認
assert round(sum(ratios.values()), 6) == 1.0, "❌ 割合の合計が100%ではありません"

# 配分を current_supply ベースで再計算
allocations = {
    k: round(current_supply * v, 6) for k, v in ratios.items()
}

# 結果をまとめる
result = {
    "mint": TOKEN_MINT,
    "initial_supply": INITIAL_SUPPLY,
    "current_supply": current_supply,
    "burned": burned,
    "allocations": allocations
}

# JSON書き出し
with open("allocation_result.json", "w") as f:
    json.dump(result, f, indent=2)

print("✅ allocation_result.json has been created.")
