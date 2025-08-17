import os
import json
import requests
from dotenv import load_dotenv
from decimal import Decimal, getcontext

# 十分な桁数を確保
getcontext().prec = 40

load_dotenv()
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
MINT = "HJwToCxFFmtnYGZMQa7rZwHAMG2evdbdXAbbQr1Jpump"

# 初期供給を Decimal で
INITIAL_SUPPLY = Decimal("1000000000")

if not HELIUS_API_KEY:
    raise Exception("❌ HELIUS_API_KEY is not set.")

url = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
headers = {"Content-Type": "application/json"}
payload = {"jsonrpc": "2.0", "id": 1, "method": "getTokenSupply", "params": [MINT]}

print("📡 Getting supply from Helius...")
resp = requests.post(url, headers=headers, json=payload, timeout=30)
resp.raise_for_status()
data = resp.json()

if "error" in data:
    raise Exception(f"❌ RPC error: {data['error']}")

try:
    v = data["result"]["value"]
    # 精度を最優先するなら amount/decimals で算出
    amount_raw = Decimal(v["amount"])           # ベース単位の総量（整数文字列）
    decimals = int(v["decimals"])               # トークンの小数桁
    current_supply = amount_raw / (Decimal(10) ** decimals)
except KeyError as e:
    raise Exception(f"❌ Unexpected RPC response shape: missing {e}")

# 焼却量
burned = (INITIAL_SUPPLY - current_supply).quantize(Decimal("1.000000"))

# 配分（現在供給量を100%とする）
ratios = {
    "Developer Lock": Decimal("0.0025"),
    "Operational Reserve": Decimal("0.0025"),
    "Marketing and Partnerships": Decimal("0.0025"),
    "Ecosystem Rewards": Decimal("0.0025"),
    "Community": Decimal("0.99"),
}

if sum(ratios.values()) != Decimal("1"):
    raise Exception("❌ The percentages do not add up to 100%")

# トークンの小数桁に合わせて丸め単位を設定
quant = Decimal(1) / (Decimal(10) ** decimals)

# まず未丸めで計算
alloc_raw = {k: (current_supply * v) for k, v in ratios.items()}

# 丸め & 誤差吸収（最後のキーで残差を調整）
alloc_rounded = {}
keys = list(alloc_raw.keys())
for k in keys[:-1]:
    alloc_rounded[k] = alloc_raw[k].quantize(quant)
# 残差を最後のカテゴリへ
sum_first = sum(alloc_rounded.values())
alloc_rounded[keys[-1]] = (current_supply - sum_first).quantize(quant)

result = {
    "mint": MINT,
    "decimals": decimals,
    "initial_supply": str(INITIAL_SUPPLY),
    "current_supply": str(current_supply),
    "burned": str(burned),
    "allocations": {k: str(v) for k, v in alloc_rounded.items()},
}

with open("moj-final-allocation.json", "w") as f:
    json.dump(result, f, indent=2)

print("✅ moj-final-allocation.json has been created.")
