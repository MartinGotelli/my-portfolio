import os
from datetime import datetime

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class GoogleSheetAPI:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    prices_by_code_cache = {}

    def get_credentials(self):
        credentials = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())
        return credentials

    def get_values_from_sheet(self):
        service = build('sheets', 'v4', credentials=self.get_credentials())

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId='1gmEHxkISBwkbGHWfd4M2x-P910kQNy2kajGegIp9kmw',
                                    range='Cotizaciones Test!A1:B').execute()

        return result.get('values', [])

    def prices_by_code(self):
        time_now_string = datetime.now().strftime('%Y%d%d%H%M')[:-1]

        if time_now_string in self.prices_by_code_cache:
            return self.prices_by_code_cache[time_now_string]
        else:
            prices_by_code = {}
            for row in self.get_values_from_sheet():
                # price_string example: $2.000,21
                price_string: str = row[1]
                price_string = price_string.replace('$', '').replace('.', '').replace(',', '.')
                price = float(price_string)
                if price > 0:
                    prices_by_code[row[0]] = price

            self.prices_by_code_cache[time_now_string] = prices_by_code
            return prices_by_code

    def price_for(self, instrument):
        return self.prices_by_code().get(instrument.code, 0)
