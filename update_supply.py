#!/usr/bin/env python3
"""
MOJ サプライ情報を Helius RPC から取得し、
moj-supply.json を自動生成・更新するスクリプト
"""

import json
import os
from datetime import datetime, timezone

import requests

# ───────────────────────────────────────────────
# .env があればローカル開発用に読み込む（CI では不要）
try:
    from dotenv import load_dotenv  # type: ignore
    if os.path.exists(".env"):
        load_dotenv()
except ModuleNotFoundError:
    # python-dotenv が無くても CI では動くので無視
    pass
# ───────────────────────────────────────────────

HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
if not HELIUS_API_KEY:
    raise EnvironmentError("❌ HELIUS_API_KEY が環境変数に設定されていません。")

TOKEN_MINT = "HJwToCxFFmtnYGZMQa7rZwHAMG2evdbdXAbbQr1Jpump"
RPC_URL = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
HEADERS = {"Content-Type": "application/json"}

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getTokenSupply",
    "params": {
        "mint": TOKEN_MINT
    }
}

resp = requests.post(RPC_URL, headers=HEADERS, json=payload, timeout=30)
resp.raise_for_status()                # HTTP エラーなら例外

data = resp.json()

# ─── レスポンス検証 ──────────────────────────────
try:
    supply = data["result"]["value"]
    amount_ui = float(supply["uiAmount"])
    decimals = int(supply["decimals"])
except (KeyError, TypeError, ValueError) as e:
    raise RuntimeError(
        "❌ 取得したレスポンス形式が予想と異なります。\n"
        f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}"
    ) from e
# ───────────────────────────────────────────────

# 例：ここでは総供給量のみ保存（必要に応じて項目を増やせます）
out = {
    "name":        "moheji",
    "symbol":      "MOJ",
    "decimals":    decimals,
    "total_supply": amount_ui,
    "last_updated": datetime.now(timezone.utc).isoformat(timespec="seconds")
}

with open("moj-supply.json", "w", encoding="utf-8") as fp:
    json.dump(out, fp, indent=2, ensure_ascii=False)

print("✅ moj-supply.json を更新しました:", out["total_supply"])
