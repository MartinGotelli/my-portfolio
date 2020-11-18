import requests

retry = 10


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def endpoint(operation):
    return "https://api.invertironline.com/" + operation


class IOLAPI(metaclass=Singleton):
    token = None
    token_for_refresh = None
    requests_count = 0
    user = None
    password = None

    def set_user_and_password(self, user, password):
        self.user = user
        self.password = password

    def requests(self):
        self.requests_count += 1
        return requests

    def get_token(self):
        if self.token is None:
            self.refresh_token()
        return self.token

    def error(self, response, financial_instrument=""):
        raise Exception(response.reason + " " + financial_instrument)

    def refresh_token(self, iteration=0):
        if self.token_for_refresh is None:
            response = self.requests().get(endpoint("token"),
                                           data={"username": self.user, "password": self.password,
                                                 "grant_type": "password"})
        else:
            response = self.requests().get(endpoint("token"), data={"refresh_token": self.token_for_refresh,
                                                                    "grant_type": "refresh_token"})
        if response.status_code == requests.codes.ok:
            self.token = response.json()["access_token"]
            self.token_for_refresh = response.json()["refresh_token"]
        elif response.status_code == requests.codes.service_unavailable and iteration < retry:
            self.refresh_token(iteration + 1)
        else:
            self.error(response)

    def token_headers(self):
        return {"Authorization": "Bearer " + self.get_token()}

    def price_for(self, financial_instrument, iteration=0):
        response = self.requests().get(endpoint("api/v2/bCBA/Titulos/" + financial_instrument.code + "/Cotizacion"),
                                       data={"simbolo": financial_instrument.code, "mercado": "bCBA", "plazo": "t2"},
                                       headers=self.token_headers())
        if response.status_code == requests.codes.ok:
            return float(response.json()["ultimoPrecio"]) / financial_instrument.price_each_quantity
        elif response.status_code == requests.codes.service_unavailable and iteration < retry:
            return self.price_for(financial_instrument, iteration + 1)
        else:
            self.error(response, financial_instrument.code)
