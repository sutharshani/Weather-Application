# coding=utf-8
# File:   Kumar_Shani_DSC510_Assignment12_1.py
# Name:   Shani Kumar
# Date:   11/12/2019
# Course: DSC-510 - Introduction to Programming
# Desc:   For your class project we will be creating an application to interacts with a webservice in order to obtain
#         data. Your program will use all of the information you’ve learned in the class in order to create a useful
#         application.
#
#         Your program must prompt the user for their city or zip code and request weather forecast data from
#         OpenWeatherMap. Your program must display the weather information in a READABLE format to the user.
#
#         1. Create a header for your program just as you have in the past.
#         2. Create a Python Application which asks the user for their zip code or city.
#         3. Use the zip code or city name in order to obtain weather forecast data from OpenWeatherMap.
#         4. Display the weather forecast in a readable format to the user.
#         5. Use comments within the application where appropriate in order to document what the program is doing.
#         6. Use functions including a main function.
#         7. Allow the user to run the program multiple times to allow them to look up weather conditions for
#         multiple locations.
#         8. Validate whether the user entered valid data. If valid data isn’t presented notify the user.
#         9. Use the Requests library in order to request data from the webservice.
#            a. Use Try blocks to ensure that your request was successful. If the connection was not successful
#            display a message to the user.
#         10. Use Python 3
#         11. Use try blocks when establishing connections to the webservice. You must print a message to the user
#         indicating whether or not the connection was successful
#         Usage:  This program is to complete assignment 12.1 requirements.
import requests
import datetime as dt


class WeatherForecast:
    """ This class can be used to get weather details. It does provide methods to retrieve weather details by City or
    ZIP code.
    """
    baseURL = "https://api.openweathermap.org/data/2.5/weather?"  # Base URL for the API call
    apiKey = "XXXXXXXXXXXXX"  # API Key for the API call

    def __init__(self):
        """ This method initializes variable of the class instance.
        """
        self.zipCode = None
        self.city = None
        self.response = None

    def getWeather(self):
        """ This method retrieves City or Zip Code details from user and then gets weather details.
        :return: no returns.
        """
        location = input("\nPlease enter zip code or city name (US Zip Code or City Name only): ")

        if location.isnumeric():  # Checking location entered is numeric or not
            self.zipCode = location  # Numeric must be zip code
            self.weatherByZip()  # Retrieve weather details by Zip Code
        else:
            self.city = location  # Otherwise location must be City Name
            self.weatherByCity()  # Retrieve weather details by City Name

    def weatherByCity(self):
        """ This method retrieves weather details by City and sets weather response from openweathermap.
        :return: no returns.
        """
        # Constructed full URL for API call.
        weatherReqURL = (self.baseURL + "APPID={}&units=imperial&q={},US").format(self.apiKey, self.city)

        # Exception handling
        try:
            self.response = requests.get(weatherReqURL)  # Perform rest request
        except Exception as e:
            print("Not able to retrieve weather information for '{}'; error - {}".format(self.city, e))

    def weatherByZip(self):
        """ This method retrieves weather details by Zip Code and sets weather response from openweathermap.
        :return: no returns.
        """
        # Constructed full URL for API call.
        weatherReqURL = (self.baseURL + "APPID={}&units=imperial&zip={},us").format(self.apiKey, self.zipCode)

        # Exception handling
        try:
            self.response = requests.get(weatherReqURL)   # Perform rest request

        except Exception as e:
            print("Not able to retrieve weather information for '{}'; error - {}".format(self.zipCode, e))

    def displayWeather(self):
        """ This routine will display weather data appropriately.
        :return: no returns.
        """
        resp = self.response.json()  # Get response json data in work field for below display purpose.

        print("\n{:-<60}".format(""))
        print("{}".format("Weather details for {}, {}").format(resp["name"], resp["sys"]["country"]).center(50))
        print("{:-<60}".format(""))
        print("\nCurrent Conditions:")
        print("{:-<60}".format(""))
        print(" {:<25}:  {}°F".format("Temperature", resp["main"]["temp"]))
        print(" {:<25}:  {}".format("Condition", resp["weather"][0]["description"]))
        if len(resp["weather"]) > 1:
            for cond in resp["weather"][1:]:
                if cond["description"]:
                    print(" {:<25}:  {}".format(" ", cond["description"]))
        if resp["main"]["pressure"] is not None:
            print(" {:<25}:  {} hPa".format("Pressure", resp["main"]["pressure"]))
        if resp["main"]["humidity"] is not None:
            print(" {:<25}:  {} %".format("Humidity", resp["main"]["humidity"]))
        if resp["wind"] is not None:
            print(" {:<25}:  {} m/s, {}°".format("Wind", resp["wind"]["speed"], resp["wind"]["deg"]))
        print("\nForecast for whole day:")
        print("{:-<60}".format(""))
        print(" {:<25}:  {}°F".format("Minimum Temp", resp["main"]["temp_min"]))
        print(" {:<25}:  {}°F".format("Maximum Temp", resp["main"]["temp_max"]))

        if (resp["sys"] is not None) & (resp["sys"]["sunrise"] is not None):
            print(" {:<25}:  {} UTC".format("Sunrise",
                                            dt.datetime.utcfromtimestamp(resp["sys"]["sunrise"], ).ctime()))
            print(" {:<25}:  {} UTC".format("Sunset",
                                            dt.datetime.utcfromtimestamp(resp["sys"]["sunset"], ).ctime()))
        print("{:-<60}".format(""))


def main():
    """ This is mainline function of this program.
    :return: no returns.
    """
    weatherObj = WeatherForecast()    # Create WeatherForecast object

    print("---: Welcome to the weather application :---")

    while True:  # Loop to add items until user want to continue

        weatherObj.__init__()
        weatherObj.getWeather()

        if weatherObj.response is not None:
            if weatherObj.response.status_code == 200:
                try:
                    weatherObj.displayWeather()
                except Exception as e:
                    print("\nError in printing the details; error - {}".format(e))
            else:
                print("Not able to retrieve weather information; error - "
                      "{}".format(weatherObj.response.json()["message"]))

        print("\n")

        decision = input("Would you like to pull weather data for different location "
                         "(enter 'Y' or 'y' to continue): ").upper()

        if decision != "Y":
            break                      # Exit from loop when decision is not 'Y' or 'y'


if __name__ == '__main__':
    main()
