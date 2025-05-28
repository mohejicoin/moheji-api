import requests
import json
from datetime import datetime

# moheji（MOJ）のTokenアドレス（例：あなたのSolanaのTokenアドレスに変更）
TOKEN_ADDRESS = "HJwToCxFFmtnYGZMQa7rZwHAMG2evdbdXAbbQr1Jpump"

# 環境変数からHELIUSのAPIキーを取得
import os
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")

# 残高取得エンドポイント
url = f"https://api.helius.xyz/v0/token-metadata?api-key={api_key}"


# 残高確認用リクエストボディ
body = {
    "mintAccounts": [TOKEN_ADDRESS]
}

response = requests.post(url, json=body)
data = response.json()

# Supply（供給量）取得（decimalsに応じて補正）
decimals = int(data[0]["decimals"])
raw_supply = int(data[0]["supply"])
supply = raw_supply / (10 ** decimals)

# JSONファイルに書き出し
output = {
    "token": "moheji",
    "symbol": "MOJ",
    "supply": supply,
    "last_updated": datetime.utcnow().isoformat() + "Z"
}

with open("moj-supply.json", "w") as f:
    json.dump(output, f, indent=2)

print("Updated moj-supply.json")
