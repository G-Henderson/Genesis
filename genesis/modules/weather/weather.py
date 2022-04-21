from utils.ModuleSettings import get_addon_settings
from utils.voice import Voice

import requests
from datetime import datetime


class Module:

    """
    Module for adjusting the volume the device
    """

    def __init__(self, command: str, args: list, voice_instance: Voice, extras) -> None:
        # Initialise variables from the arguments
        self.command = command
        self.args = args
        self.voice = voice_instance
        self.extras = extras

        # Setup other variables
        self.USER_SETTINGS = get_addon_settings("weather")
        self.UNITS = {"standard": "kelvin", "metric": "celcius", "imperial": "fahrenheit"}


    def call_api(self):
        base_url = f"https://api.openweathermap.org/data/2.5/onecall"

        params = {
            "lat": self.USER_SETTINGS["lat"],
            "lon": self.USER_SETTINGS["long"],
            "units": self.USER_SETTINGS["units"],
            "appid": self.USER_SETTINGS["api_key"],
        }

        return requests.get(base_url, params=params).json()


    def say_weather(self):
        response = self.call_api()
        now = response["current"]

        voice_output = ""

        for weather in now["weather"]:
            voice_output += (
                f"{weather['description']} "
                "with a temperature of "
                f"{now['temp'] : .0f} degrees {self.UNITS[self.USER_SETTINGS['units']]} "
            )

        # check for any alerts
        try:
            for alert in response["alert"]:
                voice_output += (
                    f"alert from {alert['sender_name']} "
                    f"{alert['event']} {alert['description']} "
                )
        except:
            pass

        # check for rain and snow
        if "rain" in now:
            voice_output += f"with {now['rain']['1h']} milimeters of rain "
        elif "snow" in now:
            voice_output += f"with {now['snow']['1h']} milimeters of snow "

        self.voice_instance.say(voice_output)


    def say_seven_day_forecast(self):
        response = self.call_api()

        daily = response["daily"]

        voice_output = ""

        for day in daily:
            for weather in day["weather"]:
                voice_output += (
                    "on "
                    f"{datetime.fromtimestamp(day['dt']).strftime('%A')} "
                    "it will be "
                    f"{weather['description']} "
                    "with a maximum temperature of "
                    f"{day['temp']['max'] : .0f} degress"
                    f"{self.UNITS[self.USER_SETTINGS['units']]} "
                    f"and minimum temperature of "
                    f"{day['temp']['min'] : .0f} degrees"
                    f"{self.UNITS[self.USER_SETTINGS['units']]}, "
                )

        self.voice_instance.say(voice_output)


    def execute_query(self):
        actions = {
            "weather": self.say_weather,
            "forecast": self.say_seven_day_forecast,
        }

        actions[self.query](self.voice_instance)


    def parse_query(self):
        query = None

        if "weather" in self.command:
            query = "weather"
        elif "forecast" in self.command:
            query = "forecast"

        return query


    # Main procedure
    def run(self) -> None:
        query = self.parse_query(self.command)
        self.execute_query(query, self.voice_instance)