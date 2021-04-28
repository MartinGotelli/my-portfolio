from datetime import datetime

from googleapiclient.discovery import build

from services.credentials_manager import CredentialsManager


class GoogleSheetAPI:
    prices_by_code_cache = {}

    @staticmethod
    def get_credentials():
        return CredentialsManager().google_credentials()

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
