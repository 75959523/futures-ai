import requests
import time
import json
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed


class OKXFetcher:
    BASE_URL = "https://www.okx.com"
    SYMBOLS = {
        "BTC": "BTC-USDT-SWAP",
        "ETH": "ETH-USDT-SWAP",
        "SOL": "SOL-USDT-SWAP"
    }

    def get_funding_rate(self, symbol):
        url = f"{self.BASE_URL}/api/v5/public/funding-rate"
        params = {"instId": symbol}
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("code") == "0" and data.get("data"):
            try:
                funding_rate = float(data["data"][0]["fundingRate"])
                timestamp_ms = int(data["data"][0]["fundingTime"])  # 资金费率时间戳
                dt_object = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
                formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
                return funding_rate, formatted_time
            except Exception:
                return None, None
        return None, None

    def compute_funding_rate_distribution(self, funding_rate):
        if funding_rate is None:
            return None
        displayed_rate = funding_rate * 100
        delta = (abs(displayed_rate) / 0.0064) * 6
        if displayed_rate > 0:
            long_pct = 50 + delta
            short_pct = 50 - delta
        else:
            long_pct = 50 - delta
            short_pct = 50 + delta
        return f"{long_pct:.2f}%:{short_pct:.2f}%"

    def get_open_interest_and_volume(self, symbol, begin, end, period="5m"):
        url = f"{self.BASE_URL}/api/v5/rubik/stat/contracts/open-interest-volume"
        params = {
            "ccy": symbol.replace("-USDT-SWAP", ""),
            "begin": str(begin),
            "end": str(end),
            "period": period
        }
        response = requests.get(url, params=params)
        return response.json()

    def extract_latest_open_interest(self, data):
        if data.get("data") and len(data["data"]) > 0:
            try:
                latest_entry = data["data"][0]  # 取第一条最新的数据
                timestamp_ms = int(latest_entry[0])  # 时间戳（毫秒）
                open_interest = float(latest_entry[1])  # 持仓量
                dt_object = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc) + timedelta(hours=8)
                formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
                return open_interest, formatted_time
            except Exception:
                return None, None
        return None, None

    def get_elite_position_ratio_contract_top_trader(self, symbol, period="5m"):
        url = f"{self.BASE_URL}/api/v5/rubik/stat/contracts/long-short-position-ratio-contract-top-trader"
        params = {
            "instId": symbol,
            "period": period
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("code") == "0" and data.get("data") and len(data["data"]) > 0:
            try:
                ratio_str = data["data"][0][1]
                return float(ratio_str)
            except Exception:
                return None
        return None

    def compute_elite_distribution(self, ratio):
        if ratio is None:
            return None
        long_pct = ratio / (1 + ratio) * 100
        short_pct = 100 - long_pct
        return f"{long_pct:.2f}%:{short_pct:.2f}%"

    def fetch_data_for_coin(self, coin, symbol, begin_time, end_time):
        oi_data = self.get_open_interest_and_volume(symbol, begin_time, end_time)
        latest_oi, oi_timestamp = self.extract_latest_open_interest(oi_data)
        funding_rate, funding_time = self.get_funding_rate(symbol)
        elite_ratio = self.get_elite_position_ratio_contract_top_trader(symbol, period="5m")

        formatted_rate = f"{funding_rate * 100:.4f}%" if funding_rate is not None else None
        funding_distribution = self.compute_funding_rate_distribution(funding_rate)
        formatted_oi = f"{latest_oi / 1e8:.2f}亿 ({oi_timestamp})" if latest_oi is not None else None
        formatted_elite = f"{elite_ratio:.4f}" if elite_ratio is not None else None
        elite_distribution = self.compute_elite_distribution(elite_ratio)

        return coin, {
            "funding_rate": formatted_rate,
            "funding_rate_time": funding_time,
            "funding_rate_distribution": funding_distribution,
            "latest_open_interest_24h": formatted_oi,
            "elite_position_ratio": formatted_elite,
            "elite_position_distribution": elite_distribution
        }

    def fetch_data(self):
        end_time = int(time.time() * 1000)
        begin_time = end_time - 24 * 60 * 60 * 1000
        result = {}
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(self.fetch_data_for_coin, coin, symbol, begin_time, end_time)
                for coin, symbol in self.SYMBOLS.items()
            ]
            for future in as_completed(futures):
                coin, data = future.result()
                result[f"OKX-{coin}"] = data
        return result


if __name__ == "__main__":
    fetcher = OKXFetcher()
    data = fetcher.fetch_data()
    print(json.dumps(data, indent=2, ensure_ascii=False))