from flask import Flask
from flask import redirect
from flask import request
import pyowm
import pytils
import requests_cache

app = Flask(__name__)

request_cache_enable = True
request_cache_timeout = 60

# class weathere:
title = "WeaThere"

class weathere:

    def webpage(self, city=None):
        if request.method == 'POST':
            city = request.form['city']
            return redirect("/today/" + pytils.translit.translify(city))
        elif city == None:
            return ("<html><head><title>"+ title +"</title></head>" \
                                                  "<h3>Hello!</h3>" \
                                                  "<b>Where do you wanna go today?</b>" \
                                                  "<br/><form method=\"post\" action=/today/>" \
                                                  "<input type=\"text\" name=\'city\'/><input type=\"submit\" />" \
                                                  "</form></html>")
        owm = pyowm.OWM('10f88ff6b5048020b0403138b9d95e13')
        try:
            observation = owm.weather_at_place(pytils.translit.translify(city) + ",ru")
            w = observation.get_weather()
            owm_temp = w.get_temperature('celsius')["temp"]
        except:
            owm_temp = False
        from weatherbit.api import Api
        api_key = "92cef175208d46c49c057bd15d7a15db"
        api = Api(api_key)
        api.set_forecast_granularity('hourly')
        try:
            forecast = api.get_current(city=pytils.translit.translify(city) + ",Ru")
            bit_temp = forecast.json["data"][0]["temp"]
        except:
            bit_temp = False
        if (bit_temp != False and owm_temp != False):
            avg_temp = sum(([owm_temp, bit_temp])) / (2)
        elif bit_temp != False:
            avg_temp = bit_temp
        elif owm_temp != False:
            avg_temp = owm_temp
        else:
            avg_temp = "No data"
        self.log(city=city, owm_temp=owm_temp, bit_temp=bit_temp, avg_temp=avg_temp)
        html = "<html><head><title>"+ title +" in " + city +"</title></head>" \
               "<h1>" + city + " " + str(avg_temp) + "&#8451;</h1>" \
               "<h2>" + pytils.translit.translify(city) + "</h2>" \
               "<h3>OWM: " + str(owm_temp) + "</h3>" \
               "<h3>WeatherBit: " + str(bit_temp) + "</h3>" \
               "<div><a href=\"/\">На главную</a>"
        return html


    def __init__(self):
        if request_cache_enable:
            requests_cache.install_cache(cache_name='weather_cache', backend='sqlite',
                                         expire_after=request_cache_timeout,
                                         allowable_codes=(200, 404, 401))


    def log(self, **data):
        msg = ''
        for key, value in data.items():
            msg += ("{}: {}; ".format(key, value))
        print(msg)

wea = weathere()

@app.route("/", methods=['POST', 'GET'])
@app.route("/today/", methods=['POST', 'GET'])
@app.route("/today/<city>")
def getSite(city=None):
    log(city=city)
    return wea.webpage(city)

def log(**data):
        msg = ''
        for key, value in data.items():
            msg += ("{}: {}; ".format(key, value))
        print(msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    if request_cache_enable:
        requests_cache.install_cache(cache_name='weather_cache', backend='sqlite',
                                     expire_after=request_cache_timeout,
                                     allowable_codes=(200, 404, 401))
