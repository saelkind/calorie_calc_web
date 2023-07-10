
import requests
from selectorlib import Extractor


class Location:
    '''Location expressed by city and country names.  Limitation of timeanddate.com -
    the site expects manual resolution of ambiguous city names, so just live without
    resolving that (e.g., Albany GA vs Albany NY
    Then use web scraping to reture the current temp there using get_temperature()'''
    # Fixed problem of http.client not found during import of requests
    # by renaming class Locale to Location.  Weird!

    #

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
    # non-breaking space
    NBSP = '\xa0'
    DEG_F = "°F"
    DEG_C = "°C"

    def __init__(self, city: str = None, country: str = None):
        if (city is None or city.strip() == "") or \
                (country is None or country.strip() == ""):
            raise ValueError("Both city and country have to be supplied")
        self.city: str = city.strip().lower().replace(" ", "-")
        self.country: str = country.strip().lower().replace(" ", "-")

    def get_temperature(self, want_metric: bool):
        '''get current temp for location, either deg F or deg C as determined by want_metric
        flag bad HTTP response by adding 1000 to the response code'''
        url = f"{Location.WEATHER_BASE_URL}/{self.country}/{self.city}"
        response = requests.get(url, headers=Location.REQUEST_HEADERS, timeout=10)
        if response.status_code != 200:
            # print(f"got bad http response status code {response.status_code}")
            return response.status_code + 1000
        extractor = Extractor.from_yaml_file("temperature.yaml")
        temp_dict = extractor.extract(response.text)
        temp_str = temp_dict['temp']
        if Location.DEG_F in temp_str:
            self.temp_F = float(temp_str.replace(f'{Location.NBSP}°F', ''))
            self.temp_C = (self.temp_F - 32) * 5.0 / 9.0
        else:
            self.temp_C = float(temp_str.replace(f'{Location.NBSP}°C', ''))
            self.temp_F = (self.temp_C * 9.0 / 5.0) + 32
        return self.temp_C if want_metric else self.temp_F


# test

location = Location(city="New City", country="USA")
print(location.country)
print(location.city)
print(f"Temp: {location.get_temperature(False):.2f}{Location.DEG_F} or {location.get_temperature(True):.2f}{Location.DEG_C}")
print()
location = Location(country="south korea", city="Seoul")
print(location.country)
print(location.city)
print(f"Temp: {location.get_temperature(False):.2f}{Location.DEG_F} or {location.get_temperature(True):.2f}{Location.DEG_C}")
print()
# usa is the correct country name
location = Location(city="New City", country="US")
print(location.country)
print(location.city)
print(f"Temp: {location.get_temperature(False):.2f}{Location.DEG_F} or {location.get_temperature(True):.2f}{Location.DEG_C}")
print()
# uk is the correct country name
location = Location(city="Glasgow", country="scotland")
print(location.country)
print(location.city)
print(f"Temp: {location.get_temperature(False):.2f}{Location.DEG_F} or {location.get_temperature(True):.2f}{Location.DEG_C}")
print()
# uk is the correct country name
location = Location(city="Glasgow", country="uk")
print(location.country)
print(location.city)
print(f"Temp: {location.get_temperature(False):.2f}{Location.DEG_F} or {location.get_temperature(True):.2f}{Location.DEG_C}")
print()
