import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む（事前にpip install python-dotenv）
load_dotenv()

# 環境変数からAPIキー取得
api_key = os.getenv("7c8afe86-b590-4fa8-8e49-99d0f751d63c")
if not api_key:
    raise EnvironmentError("❌ 環境変数 'HELIUS_API_KEY' が設定されていません")

# MOJトークンのMintアドレス
TOKEN_ADDRESS = "HJwToCxFFmtnYGZMQa7rZwHAMG2evdbdXAbbQr1Jpump"

# APIエンドポイント
url = f"https://api.helius.xyz/v0/token-metadata?api-key={api_key}"

# リクエストボディ
body = {
    "mintAccounts": [TOKEN_ADDRESS]
}

try:
    response = requests.post(url, json=body)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"❌ APIリクエスト失敗: {e}")
    raise

# レスポンス取得
data = response.json()

if not data:
    raise ValueError(f"❌ APIのレスポンスにトークンデータが含まれていません: {data}")

token_data = data[0]

if "decimals" not in token_data or "supply" not in token_data:
    raise KeyError(f"❌ 'decimals' または 'supply' がレスポンスに含まれていません: {token_data}")

# 供給量の計算
decimals = int(token_data["decimals"])
raw_supply = int(token_data["supply"])
supply = raw_supply / (10 ** decimals)

# 出力データ
output = {
    "token": "moheji",
    "symbol": "MOJ",
    "supply": round(supply, 6),  # 小数点以下6桁に丸める
    "last_updated": datetime.utcnow().isoformat() + "Z"
}

# JSONファイルとして保存
with open("moj-supply.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("✅ moj-supply.json を更新しました")

