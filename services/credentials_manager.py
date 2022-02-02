import json
import os

from cryptography.fernet import Fernet
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

FERNET_INI = 'fernet_key.ini'
IOL_INI = 'IOL_credentials.ini'


class CredentialsManager:
    def __init__(self):
        self.credentials = {}

    @staticmethod
    def get_iol_credentials():
        if not os.path.exists(FERNET_INI) or not os.path.exists(IOL_INI):
            raise Exception('There are no IOL credentials configured')
        else:
            with open(FERNET_INI, 'r') as key_file:
                fernet_key = bytes(key_file.read(), 'utf-8')

            with open(IOL_INI, 'r') as iol_ini:
                return json.loads(Fernet(fernet_key).decrypt(bytes(iol_ini.read(), 'utf-8')))

    def iol_credentials(self):
        return self.credentials.setdefault('IOL', self.get_iol_credentials())

    def iol_username(self):
        return self.iol_credentials()["user"]

    def iol_password(self):
        return self.iol_credentials()["password"]

    def get_google_credentials(self):
        credentials = None
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json', scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                try:
                    credentials.refresh(Request())
                except RefreshError:
                    # We delete the token to create once again
                    os.remove('token.json')
                    return self.get_google_credentials()
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
                credentials = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())
        return credentials

    def google_credentials(self):
        return self.credentials.setdefault('GOOGLE', self.get_google_credentials())
