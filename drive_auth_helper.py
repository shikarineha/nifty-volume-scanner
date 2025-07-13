# drive_auth_helper.py

from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

# Scopes: grants access to upload files created by this script
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def main():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

if __name__ == '__main__':
    main()
