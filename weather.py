from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os
import requests
import geonamescache


def load_api():
    key = '0'

    if os.path.exists('api_key.txt'):
        file = open('api_key.txt')
        key = file.read()
        file.close()

    return key


class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setFixedSize(600, 600)

        self.key_label = QLineEdit(self)
        self.key_label.setPlaceholderText('API Key')
        self.key_label.setGeometry(150, 400, 300, 25)

        self.load_btn = QPushButton(self)
        self.load_btn.setText('Load Key')
        self.load_btn.setGeometry(225, 475, 150, 30)
        self.load_btn.setFocusPolicy(Qt.NoFocus)


class ClientWindow(QWidget):
    def __init__(self, parent=None):
        super(ClientWindow, self).__init__(parent)

        self.API_KEY = '0'
        self.POLL_INT = 5000
        self.CITY_NAME = ''
        self.latitude = ''
        self.longitude = ''

        # setting window style
        self.setFixedSize(600, 600)

        self.weather_label = QTextEdit(self)
        self.weather_label.setReadOnly(True)
        self.weather_label.setGeometry(150, 50, 300, 300)

        # setting window widgets
        self.city_label = QComboBox(self)
        self.city_label.setEditable(True) # add city label with picture
        self.city_label.setGeometry(150, 400, 300, 25)
        self.city_label.currentTextChanged.connect(self._update_combo)

        self.lat_box = QLineEdit(self)
        self.lat_box.setPlaceholderText('Latitude')
        self.lat_box.setGeometry(200, 400, 75, 25)
        self.lat_box.hide()

        self.long_box = QLineEdit(self)
        self.long_box.setPlaceholderText('Longitude')
        self.long_box.setGeometry(325, 400, 75, 25)
        self.long_box.hide()

        self.toggle = QCheckBox(self)
        self.toggle.setGeometry(500, 400, 25, 25)
        self.toggle.clicked.connect(self._toggle_coordinates)

        self.timer = QTimer(self)
        self.timer.setInterval(self.POLL_INT)
        self.timer.timeout.connect(self._tmr_get_weather)

        load_btn = QPushButton(self)
        load_btn.setText('Get Weather Data')
        load_btn.setGeometry(225, 475, 150, 30)
        load_btn.clicked.connect(self._get_weather)
        load_btn.setFocusPolicy(Qt.NoFocus)

    def _update_combo(self):

        u_input = self.city_label.currentText()
        gc = geonamescache.GeonamesCache()
        cities = gc.get_cities_by_name(u_input)

        if len(cities) == 0:
            return

        self.city_label.clear()
        i = 0
        while i < 3 and i < len(cities):
            place = list(cities[i].values())
            name = place[0].get('name')
            code = place[0].get('countrycode')
            admin_label = place[0].get('admin1code')
            lat = place[0].get('latitude')
            long = place[0].get('longitude')

            city = name + ', ' + admin_label + ', ' + code + ', (' + str(lat) + '°, ' + str(long) + '°)'
            self.city_label.addItem(city)
            i += 1

        self.city_label.update()

    def _toggle_coordinates(self):

        self.lat_box.clear()
        self.long_box.clear()
        self.city_label.clear()

        if self.toggle.isChecked():
            self.city_label.hide()
            self.lat_box.show()
            self.long_box.show()
        else:

            self.city_label.show()
            self.lat_box.hide()
            self.long_box.hide()

    def _tmr_get_weather(self):
        # check for empty things
        if self.toggle.isChecked():
            if len(self.latitude) != 0:
                self._coordinate_query(self.latitude, self.longitude)
            elif len(self.CITY_NAME) != 0:
                self._name_query(self.CITY_NAME)
        else:
            if len(self.CITY_NAME) != 0:
                self._name_query(self.CITY_NAME)
            elif len(self.latitude) != 0:
                self._coordinate_query(self.latitude, self.longitude)

    def _check_valid_lat_long(self, latitude, longitude):

        if latitude.isalpha() or longitude.isalpha():
            QMessageBox.warning(self, 'Weather Search Failed', 'Invalid latitude and/or longitude')
            self.lat_box.clear()
            self.long_box.clear()
            return False

        elif len(latitude) == 0 and len(longitude) == 0:
            return False

        elif len(latitude) == 0 or len(longitude) == 0:
            QMessageBox.warning(self, 'Weather Search Failed', 'Invalid latitude and/or longitude')
            self.lat_box.clear()
            self.long_box.clear()
            return False

        else:
            return True

    def _get_weather(self):
        if self.toggle.isChecked():
            if self._check_valid_lat_long(self.lat_box.text(), self.long_box.text()):
                self._coordinate_query(self.lat_box.text(), self.long_box.text())
        else:
            self._name_query(self.city_label.currentText())

    def _coordinate_query(self, latitude, longitude):

        if len(latitude) == 0 or len(longitude) == 0:
            return

        weather_url = 'https://api.openweathermap.org/data/2.5/weather?lat=' + latitude + '&lon=' + longitude + \
                      '&appid=' + self.API_KEY

        # Get the response from fetched url
        response = requests.get(weather_url)

        # changing response from json to python readable
        weather_info = response.json()

        # as per API documentation, if the cod is 200, it means that weather data was successfully fetched

        if weather_info['cod'] == 200:

            self.weather_label.clear()

            temp = int((weather_info['main']['temp'] - 273) * 9 / 5 + 32)  # converting default kelvin value to Celcius
            feels_like_temp = int((weather_info['main']['feels_like'] - 273) * 9 / 5 + 32)
            pressure = weather_info['main']['pressure']
            humidity = weather_info['main']['humidity']
            wind_speed = weather_info['wind']['speed'] * 3.6
            clouds = weather_info['clouds']['all']
            sunrise = weather_info['sys']['sunrise']
            sunset = weather_info['sys']['sunset']

            self.weather_label.insertPlainText('Lat: ' + latitude + ' Lon: ' + longitude + '\n')
            self.weather_label.insertPlainText('=======================\n')
            self.weather_label.insertPlainText('Temperature: ' + str(temp) + ' °F\n')
            self.weather_label.insertPlainText('Feels Like Temperature: ' + str(feels_like_temp) + ' °F\n')
            self.weather_label.insertPlainText('Pressure: ' + str(pressure) + ' mb\n')
            self.weather_label.insertPlainText('Humidity: ' + str(humidity) + ' %\n')
            self.weather_label.insertPlainText('Wind Speed: ' + str(wind_speed) + ' km/h\n')
            self.weather_label.insertPlainText('Cloud Coverage: ' + str(clouds) + ' %\n')

            self.CITY_NAME = ''
            self.latitude = latitude
            self.longitude = longitude

        else:
            QMessageBox.warning(self, 'Weather Search Failed', 'Could not find weather information for the given '
                                                               'coordinates.')

        print('made coordinate query')

    def _name_query(self, name):

        if len(name) == 0:
            return

        city_name = name

        weather_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city_name + \
                      '&appid=' + self.API_KEY

        # Get the response from fetched url
        response = requests.get(weather_url)

        # changing response from json to python readable
        weather_info = response.json()

        # as per API documentation, if the cod is 200, it means that weather data was successfully fetched

        if weather_info['cod'] == 200:

            self.weather_label.clear()

            temp = int((weather_info['main']['temp'] - 273) * 9 / 5 + 32)  # converting default kelvin value to Celcius
            feels_like_temp = int((weather_info['main']['feels_like'] - 273) * 9 / 5 + 32)
            pressure = weather_info['main']['pressure']
            humidity = weather_info['main']['humidity']
            wind_speed = weather_info['wind']['speed'] * 3.6
            clouds = weather_info['clouds']['all']
            sunrise = weather_info['sys']['sunrise']
            sunset = weather_info['sys']['sunset']

            self.weather_label.insertPlainText(city_name + '\n')
            self.weather_label.insertPlainText('=======================\n')
            self.weather_label.insertPlainText('Temperature: ' + str(temp) + ' °F\n')
            self.weather_label.insertPlainText('Feels Like Temperature: ' + str(feels_like_temp) + ' °F\n')
            self.weather_label.insertPlainText('Pressure: ' + str(pressure) + ' mb\n')
            self.weather_label.insertPlainText('Humidity: ' + str(humidity) + ' %\n')
            self.weather_label.insertPlainText('Wind Speed: ' + str(wind_speed) + ' km/h\n')
            self.weather_label.insertPlainText('Cloud Coverage: ' + str(clouds) + ' %\n')
            self.weather_label.insertPlainText('Sunrise: ' + str(sunrise) + '\n')
            self.weather_label.insertPlainText('Sunset: ' + str(sunset) + '\n')

            self.CITY_NAME = city_name
            self.latitude = ''
            self.longitude = ''

        else:
            QMessageBox.warning(self, 'Weather Search Failed', 'Could not find weather information for ' + city_name)

        print('made name query')

    def _start(self):
        self.timer.start()

    def _stop(self):
        self.timer.stop()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.API = load_api()

        if self.API == '0':
            self._startLoginWindow()
        else:
            self._startClientWindow()

    def _startLoginWindow(self):
        self.login = LoginWindow()
        self.setWindowTitle('SolAce API Login')
        self.setCentralWidget(self.login)
        self.login.load_btn.clicked.connect(self._check_pass)
        self.show()

    def _startClientWindow(self):
        self.client = ClientWindow()
        self.client._start()
        self.client.API_KEY = self.API

        self.setWindowTitle('SolAce')
        self.setCentralWidget(self.client)
        self.show()

    def _check_pass(self):

        api_key = self.login.key_label.text()
        weather_url = 'https://api.openweathermap.org/data/2.5/weather?q=Paris&appid=' + api_key

        try:
            response = requests.get(weather_url)

            if response.status_code != 200:
                QMessageBox.warning(self, 'Authentication Failed', 'Invalid API Key. '
                                                                   'Try again with a different key')
                self.login.key_label.clear()

            else:
                file = open('api_key.txt', "x")
                file.write(api_key)

                self._startClientWindow()

        except requests.exceptions.ConnectionError:
            QMessageBox.warning(self, 'API Authentication Failed',
                                "Could not connect to API Authentication Service. Check your internet "
                                "connection.")
            self.login.key_label.clear()