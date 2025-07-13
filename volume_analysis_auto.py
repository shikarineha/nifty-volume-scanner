from login_utils import login

smart_api = login()

if smart_api:
    print("🎯 Proceed with analysis logic here")
else:
    print("🚫 Cannot proceed due to login failure")
