# smartapi_login.py
import pyotp
from SmartApi.smartConnect import SmartConnect
from credentials import API_KEY, CLIENT_CODE, MPIN, TOTP_SECRET

def generate_token():
    totp = pyotp.TOTP(TOTP_SECRET).now()
    obj = SmartConnect(api_key=API_KEY)

    try:
        data = obj.loginWithMPIN(CLIENT_CODE, MPIN, totp)
        obj.setAccessToken(data['data']['access_token'])
        return obj
    except Exception as e:
        print("❌ Login failed:", e)
        return None
