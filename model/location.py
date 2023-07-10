import requests
from selectorlib import Extractor
from string import capwords as capwords


class Location:
    '''Location expressed by city and country names.  Limitation of timeanddate.com -
    the site expects manual resolution of ambiguous city names, so just live without
    resolving that (e.g., Albany GA vs Albany NY
    Then use web scraping to return the current temp there using get_temperature()'''
    # Fixed problem of http.client not found during import of requests
    # by renaming class Locale to Location.  Weird!

    WEATHER_BASE_URL = "https://www.timeanddate.com/weather/"
    # headers provided by ardit cluice
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
    METRIC_KEY = "metric"
    ENGLISH_KEY = "English"
    STATUS_KEY = "status"
    GOOD_DATA_KEY = "good data"

    def __init__(self, city: str = None, country: str = None):
        if (city is None or city.strip() == "") or \
                (country is None or country.strip() == ""):
            raise ValueError("Both city and country have to be supplied")
        self.city: str = city.strip().lower().replace(" ", "-")
        self.country: str = country.strip().lower().replace(" ", "-")
        self.country_pretty:str = country.strip()
        self.country_pretty = capwords(self.country_pretty, sep=" ")
        self.city_pretty: str = city.strip()
        self.city_pretty = capwords(self.city_pretty, sep=" ")

    def get_temperature(self) -> dict:
        '''get current temp for location by scraping the timeanddate.com web site,
        returning a dict with both deg F and deg C as determined by want_metric
        flag bad HTTP response by adding 1000 to the response code'''
        url = f"{Location.WEATHER_BASE_URL}/{self.country}/{self.city}"
        response = requests.get(url, headers=Location.REQUEST_HEADERS, timeout=10)
        if response.status_code != 200:
            # print(f"got bad http response status code {response.status_code}")
            bad_return_temp = response.status_code + 1000
            return {Location.METRIC_KEY: bad_return_temp,
                    Location.ENGLISH_KEY: bad_return_temp,
                    Location.STATUS_KEY: response.status_code,
                    Location.GOOD_DATA_KEY: False}
        extractor = Extractor.from_yaml_file("temperature.yaml")
        temp_dict = extractor.extract(response.text)
        temp_str = temp_dict['temp']
        if Location.DEG_F in temp_str:
            self.temp_F = float(temp_str.replace(f'{Location.NBSP}°F', ''))
            self.temp_C = (self.temp_F - 32) * 5.0 / 9.0
        else:
            self.temp_C = float(temp_str.replace(f'{Location.NBSP}°C', ''))
            self.temp_F = (self.temp_C * 9.0 / 5.0) + 32
        return {Location.METRIC_KEY: self.temp_C,
                Location.ENGLISH_KEY: self.temp_F,
                Location.STATUS_KEY: response.status_code,
                Location.GOOD_DATA_KEY: True}


# test
if __name__ == "__main__":
    locations = [["New City", "USA"], ["Seoul", "south korea"], ["New City", "US"], \
        ["Glasgow", "scotland"], ["Glasgow", "uk"]]
    for loc in locations:
        location = Location(city=loc[0], country=loc[1])
        print(f"{location.country} -- {location.country_pretty}")
        print(f"{location.city} -- {location.city_pretty}")
        temp_resp: dict = location.get_temperature()
        print(f"Temp: {temp_resp.get(Location.ENGLISH_KEY):.2f}{Location.DEG_F} or " +
            f"{temp_resp.get(Location.METRIC_KEY):.2f}{Location.DEG_C}")
        print("HTTP response status:", temp_resp.get(Location.STATUS_KEY),
              ", Good data:", temp_resp.get(Location.GOOD_DATA_KEY))
        print()
