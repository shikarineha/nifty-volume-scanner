# login_utils.py
from SmartApi.smartConnect import SmartConnect
import pyotp
from credentials import API_KEY, CLIENT_CODE, MPIN, TOTP_SECRET

def login():
    try:
        obj = SmartConnect(api_key=API_KEY)
        totp = pyotp.TOTP(TOTP_SECRET).now()
        
        # Use the correct login method
        response = obj.loginWithMPIN(CLIENT_CODE, MPIN, totp)

        if response['status']:
            print("✅ Login successful.")
            obj.setAccessToken(response['data']['access_token'])
            return obj
        else:
            print(f"❌ Login failed: {response.get('message')}")
            return None

    except Exception as e:
        print("❌ Login failed:", str(e))
        return None
