import os
import requests
import geonamescache


def check_valid_lat_long(latitude, longitude):
    if latitude.isalpha() or longitude.isalpha():
        return False
    elif len(latitude) == 0 and len(longitude) == 0:
        return False
    elif len(latitude) == 0 or len(longitude) == 0:
        return False
    else:
        return True


class Weather:
    def __init__(self):
        if not self.load_api():
            self.API_KEY = input('Input API key: ')
            if not self._check_key():
                print('Invalid Key!!!')
                exit(-1)

    def load_api(self):
        if os.path.exists('api_key.txt'):
            file = open('api_key.txt')
            self.API_KEY = file.read()
            file.close()
            return True
        else:
            return False

    def coordinate_query(self, latitude, longitude):

        if check_valid_lat_long(latitude, longitude) is False:
            return 'Invalid coordinates entered', 400

        if len(latitude) == 0 or len(longitude) == 0:
            return 'No coordinates entered.', 400
            # figure out how to fix so that when they're empty it doesn't do anything

        weather_url = 'https://api.openweathermap.org/data/2.5/weather?lat=' + latitude + '&lon=' + longitude + \
                      '&appid=' + self.API_KEY

        # Get the response from fetched url
        response = requests.get(weather_url)

        # changing response from json to python readable
        weather_info = response.json()

        # as per API documentation, if the cod is 200, it means that weather data was successfully fetched

        if weather_info['cod'] == 200:

            temp = int((weather_info['main']['temp'] - 273) * 9 / 5 + 32)  #kelvin to f
            feels_like_temp = int((weather_info['main']['feels_like'] - 273) * 9 / 5 + 32) #kelvin to f
            pressure = weather_info['main']['pressure']
            humidity = weather_info['main']['humidity']
            wind_speed = weather_info['wind']['speed'] * 3.6 #m/s to km/h
            clouds = weather_info['clouds']['all']
            sunrise = weather_info['sys']['sunrise']
            sunset = weather_info['sys']['sunset']

            weather_report = 'Lat: ' + latitude + ' Lon: ' + longitude + '\n' + '=======================\n' + \
                             'Temperature: ' + str(temp) + ' °F\n ' + 'Feels Like Temperature: ' + \
                             str(feels_like_temp) + ' °F\n' + 'Pressure: ' + str(pressure) + ' mb\n' + \
                             'Humidity: ' + str(humidity) + ' %\n' + 'Wind Speed: ' + str(wind_speed) + ' km/h\n' + \
                             'Cloud Coverage: ' + str(clouds) + ' %\n'

            return weather_report, 200
        else:
            warning = 'Weather Search Failed: Could not find weather information for the given coordinates.'
            return warning, 404

    def name_query(self, city_name):

        if len(city_name) == 0:
            return 'No name entered', 400

        weather_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city_name + \
                      '&appid=' + self.API_KEY

        # Get the response from fetched url
        response = requests.get(weather_url)

        # changing response from json to python readable
        weather_info = response.json()

        # as per API documentation, if the cod is 200, it means that weather data was successfully fetched

        if weather_info['cod'] == 200:

            temp = int((weather_info['main']['temp'] - 273) * 9 / 5 + 32)  # converting default kelvin value to Celcius
            feels_like_temp = int((weather_info['main']['feels_like'] - 273) * 9 / 5 + 32)
            pressure = weather_info['main']['pressure']
            humidity = weather_info['main']['humidity']
            wind_speed = weather_info['wind']['speed'] * 3.6
            clouds = weather_info['clouds']['all']
            sunrise = weather_info['sys']['sunrise']
            sunset = weather_info['sys']['sunset']

            weather_report = city_name + '\n' + '=======================\n' + \
                             'Temperature: ' + str(temp) + ' °F\n ' + 'Feels Like Temperature: ' + \
                             str(feels_like_temp) + ' °F\n' + 'Pressure: ' + str(pressure) + ' mb\n' + \
                             'Humidity: ' + str(humidity) + ' %\n' + 'Wind Speed: ' + str(wind_speed) + ' km/h\n' + \
                             'Cloud Coverage: ' + str(clouds) + ' %\n'

            return weather_report, 200
        else:
            warning = 'Weather Search Failed: Could not find weather information for the given city.'
            return warning, 404

    def _check_key(self):

        api_key = self.API_KEY
        weather_url = 'https://api.openweathermap.org/data/2.5/weather?q=Paris&appid=' + api_key

        try:
            response = requests.get(weather_url)

            if response.status_code != 200:
                # return ('Authentication Failed: Invalid API Key. Try again with a different key',
                #         response.status_code)
                return False
            else:
                file = open('api_key.txt', "x")
                file.write(api_key)
                return True

        except requests.exceptions.ConnectionError:
            # return ('API Authentication Failed: Could not connect to API Authentication Service. Check your '
            #         'internet connection ', response.status_code)
            return False
