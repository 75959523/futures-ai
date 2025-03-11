import json
import requests

OKX_API_URL = "https://www.okx.com/api/v5/public/instruments"

def fetch_instruments():
    params = {
        "instType": "SWAP",
        "instId": "BTC-USDT-SWAP"
    }
    response = requests.get(OKX_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        print("收到数据:", json.dumps(data, indent=4, ensure_ascii=False))

        # 解析数据，输出所有字段
        if "data" in data:
            for instrument in data["data"]:
                print("合约数据:")
                for key, value in instrument.items():
                    print(f"{key}: {value}")
    else:
        print(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")

if __name__ == "__main__":
    fetch_instruments()