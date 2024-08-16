import requests


class IPGeolocation:
    def __init__(self):
        self.api_url = "https://ipinfo.io/"

    def get_current_location(self):
        try:
            response = requests.get(self.api_url)
            data = response.json()
            if 'loc' in data:
                lat, lon = map(float, data['loc'].split(','))
                return lat, lon
            else:
                return 0.0, 0.0
        except Exception as e:
            print(f"Error getting IP-based location: {e}")
            return 0.0, 0.0
