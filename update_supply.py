import requests
import json
import os
from dotenv import load_dotenv

# .env から環境変数を読み込む
load_dotenv()
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")

# トークンのミントアドレスと初期供給量
TOKEN_MINT = "HJwToCxFFmtnYGZMQa7rZwHAMG2evdbdXAbbQr1Jpump"
INITIAL_SUPPLY = 1_000_000_000.0  # 10億枚

if not HELIUS_API_KEY:
    raise Exception("❌ HELIUS_API_KEY is not set in your .env file.")

# Helius RPC 経由で現在の供給量を取得
url = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
headers = {"Content-Type": "application/json"}
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getTokenSupply",
    "params": [TOKEN_MINT],
}

print("📡 Fetching current supply from Helius API...")
response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()
data = response.json()

# 現在の供給量
current_supply = float(data["result"]["value"]["uiAmount"])
burned = round(INITIAL_SUPPLY - current_supply, 6)

print(f"✅ Current supply: {current_supply}")
print(f"🔥 Burned amount: {burned}")

# 再配分比率（burnを除外して100%配分）
ratios = {
    "Developer Lock": 0.10,
    "Operational Reserve": 0.15,
    "Marketing and Partnerships": 0.10,
    "Ecosystem Rewards": 0.10,
    "Community": 0.55
}

# 各カテゴリへの配分計算（current_supplyベース）
allocations = {
    name: round(current_supply * ratio, 6)
    for name, ratio in ratios.items()
}

# 結果を辞書にまとめる
result = {
    "mint": TOKEN_MINT,
    "initial_supply": INITIAL_SUPPLY,
    "current_supply": current_supply,
    "burned": burned,
    "allocations": allocations
}

# JSONファイルとして保存
with open("moj-final-allocation.json", "w") as f:
    json.dump(result, f, indent=2)

print("✅ moj-final-allocation.json has been created successfully.")
