import requests
from selectorlib import Extractor


class Locale:

    # Limitation - the site expects manual resolution of ambiguous city names,
    # so just live without resolving that.

    WEATHER_BASE_URL = "https://www.timeanddate.com/weather/"
    REQUEST_HEADERS = {
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    DEG_F = "°F"
    DEG_C = "°C"

    def __init__(self, city: str = None, country: str = None):
        if (city is None or city.strip() == "") or \
                (country is None or country.strip() == ""):
            raise ValueError("Both city and country have to be supplied")
        self.city: str = city.strip().lower().replace(" ", "-")
        self.country: str = country.strip().lower().replace(" ", "-")

    def get_temperature(self, want_metric: bool):
        url = f"{Locale.WEATHER_BASE_URL}/{self.country}/{self.city}xx"
        response = requests.get(url, headers=Locale.REQUEST_HEADERS, timeout=10)
        if response.status_code == 404:
            print(f"location not found (response status code 404 - not found")
            return 1000 + 404
        elif response.status_code != 200:
            print(f"got bad response status code {response.status_code}")
            return response.status_code + 1000
        extractor = Extractor.from_yaml_file("temperature.yaml")
        temp_dict = extractor.extract(response.text)
        temp_str = temp_dict['temp']
        if Locale.DEC_F in temp_str:
            self.temp_F = temp_str.replace('\xa0°F', '')
            self.temp_C = (self.temp_F - 32) * 9.0 / 5.0
        else:
            self.temp_C = temp_str.replace('\xa0°C', '')
            self.temp_F = (self.temp_C * 5.0 / 9.0) + 32
        return self.temp_C if want_metric else self.temp_F



# test

locale = Locale(city="New City", country="US")
print(locale.country)
print(locale.city)
print()
locale = Locale(country="south korea", city="Seoul")
print(locale.country)
print(locale.city)

print(f"Temp: {locale.get_temperature(False)}{Locale.DEG_F} or locale.get_temperature(True){Locale.DEG_F}")
