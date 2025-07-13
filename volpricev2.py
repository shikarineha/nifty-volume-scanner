import requests
import datetime
import pyotp
from logzero import logger
import socket
import uuid
import json
import pandas as pd
import numpy as np

# ✅ HARDCODED credentials
HISTORICAL_API_KEY = "X1q82Ysv"
CLIENT_CODE = "AAAO662742"
MPIN = "3010"
TOTP_SECRET = "IWXYJI7S26EUXGNWB4OCNHUQ7A"

# 📌 Target stock
STOCK = {"symbol": "SBIN-EQ", "token": "3045"}

def login(api_key):
    try:
        totp = pyotp.TOTP(TOTP_SECRET).now()
    except Exception as e:
        logger.error("Invalid Token: The provided token is not valid.")
        raise e

    payload = {
        "clientcode": CLIENT_CODE,
        "password": MPIN,
        "totp": totp,
        "state": "nifty_volume_script"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-UserType": "USER",
        "X-SourceID": "WEB",
        "X-ClientLocalIP": socket.gethostbyname(socket.gethostname()),
        "X-ClientPublicIP": "192.168.1.1",
        "X-MACAddress": ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                                     for ele in range(0, 8*6, 8)][::-1]),
        "X-PrivateKey": api_key
    }

    response = requests.post(
        url="https://apiconnect.angelone.in/rest/auth/angelbroking/user/v1/loginByPassword",
        headers=headers,
        data=json.dumps(payload)
    )

    data = response.json()
    if not data.get("status"):
        logger.error(f"Login failed: {data}")
        return None

    access_token = data["data"].get("jwtToken")
    if not access_token:
        logger.error("Login response did not return jwtToken.")
        return None

    logger.info("\u2705 Login successful.")
    return access_token

def fetch_1year_candles(symbol, token, historical_access_token):
    headers = {
        "Authorization": f"Bearer {historical_access_token}",
        "X-PrivateKey": HISTORICAL_API_KEY,
        "X-SourceID": "WEB",
        "X-ClientLocalIP": socket.gethostbyname(socket.gethostname()),
        "X-ClientPublicIP": "192.168.1.1",
        "X-MACAddress": ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                                  for ele in range(0, 8*6, 8)][::-1]),
        "X-UserType": "USER",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    url = "https://apiconnect.angelone.in/rest/secure/angelbroking/historical/v1/getCandleData"
    from_date = (datetime.datetime.now() - datetime.timedelta(days=380)).strftime("%Y-%m-%d") + " 09:15"
    to_date = datetime.datetime.now().strftime("%Y-%m-%d") + " 15:30"

    payload = {
        "exchange": "NSE",
        "symboltoken": token,
        "interval": "ONE_DAY",
        "fromdate": from_date,
        "todate": to_date
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code != 200:
            logger.warning(f"[{symbol}] HTTP {response.status_code} from historical API.")
            return []

        data = response.json()
        candles = data.get("data", [])
        return candles

    except Exception as e:
        logger.warning(f"[{symbol}] Exception while fetching historical candles: {e}")
        return []

def calculate_averages(candles):
    df = pd.DataFrame(candles, columns=["datetime", "open", "high", "low", "close", "volume"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df.set_index("datetime", inplace=True)
    df = df.sort_index()

    periods = {
        "1Y": 252,
        "10M": 210,
        "9M": 189,
        "8M": 168,
        "7M": 147,
        "6M": 126,
        "5M": 105,
        "4M": 84,
        "3M": 63,
        "2M": 42,
        "1M": 21,
        "15D": 15,
        "7D": 7
    }

    averages = {}
    for label, period in periods.items():
        if len(df) >= period:
            avg_vol = round(df["volume"].tail(period).mean(), 2)
            avg_close = round(df["close"].tail(period).mean(), 2)
            ema_vol = round(df["volume"].ewm(span=period).mean().iloc[-1], 2)
            ema_close = round(df["close"].ewm(span=period).mean().iloc[-1], 2)
        else:
            avg_vol = ema_vol = avg_close = ema_close = "N/A"

        averages[label] = {
            "SMA_Volume": avg_vol,
            "EMA_Volume": ema_vol,
            "SMA_Close": avg_close,
            "EMA_Close": ema_close
        }

    return averages

def main():
    historical_access_token = login(HISTORICAL_API_KEY)
    if not historical_access_token:
        return

    candles = fetch_1year_candles(STOCK["symbol"], STOCK["token"], historical_access_token)
    if not candles:
        return

    averages = calculate_averages(candles)
    print(f"\nAverages for {STOCK['symbol']}:\n")
    for period, data in averages.items():
        print(f"{period}: {data}")

if __name__ == "__main__":
    main()
