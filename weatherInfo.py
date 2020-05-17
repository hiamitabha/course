import requests
import jenkspy
import json
import threading
import anki_vector
import time
from anki_vector.events import Events
from anki_vector.user_intent import UserIntent, UserIntentEvent


_KEY =  'edf2a2443990c073b3d99f95818a0765'
_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
_ONECALL_URL = 'http://api.openweathermap.org/data/2.5/onecall'

def getWeatherReport(location):
   """Get the weather report for a location
   @param location Location in text
   """

   _PARAMS = {'q': location,
              'APPID': _KEY}

   r = requests.get(url=_WEATHER_URL, params=_PARAMS)
   resultWeather = r.json()

   (lat, long) = (resultWeather['coord']['lat'], resultWeather['coord']['lon'])

   _PARAMS = {'lat': lat,
              'lon': long,
              'APPID': _KEY,
     'units': 'imperial'}
   r = requests.get(url=_ONECALL_URL, params=_PARAMS)

   resultOneCall = r.json()
   return (resultWeather, resultOneCall)

def getLongestBreak(data):
   breaks = jenkspy.jenks_breaks(data, nb_class=3)
   numItemsInEachBreak = []
   breakValue = breaks[1]
   numItems = 0
   for item in data:
      if item <= breakValue:
         numItems += 1
      else:
         numItemsInEachBreak.append(numItems)
         numItems = 1
         breakValue = breaks[len(numItemsInEachBreak) + 1]
   numItemsInEachBreak.append(numItems)
   maxIndex = numItemsInEachBreak.index(max(numItemsInEachBreak))
   longestBreak = (breaks[maxIndex], breaks[maxIndex + 1])
   return (longestBreak)

def firstNonZeroIndexAndValue(data):
   index = 0
   for val in data:
      if (val > 0):
         return (index, val)
      index += 1
   return (-1, -1)

def turnIndexToDay(index):
   if index == 0:
      return ("today")
   elif index == 1:
      return ("tomorrow")
   else:
      return ("in % days" % index)

def translateToAnimation(weatherCode):
   if weatherCode == 5:
      return ('anim_weather_rain_01')
   elif weatherCode == 8:
      return ('anim_weather_cloud_01')
   elif weatherCode == 9:
      return ('anim_weather_sunny_01')
   elif weatherCode == 2:
      return ('anum_weather_thunderstorm_01')
   elif weatherCode == 6:
      return ('anim_weather_snow_01')
   elif weatherCode == 3:
      return ('anim_weather_rain_01')

def processWeather(location):
   """Processes the weather of a specified location and returns a summary in text
   and an animation
   """
   summary = [] 
   daysSinceOrigin = []
   timeSinceOrigin = []
   windSpeed = []
   humidity = []
   temp = []
   feelsLike = []
   rain = []
   uvi = []
   snow = []
   clouds = []
   weather = []
   originTime = None
   (resultWeather, resultOneCall) = getWeatherReport(location)

   for item in resultOneCall['hourly']:
      if not originTime:
         originTime = item['dt']
         timeSinceOrigin.append(0)
      else:
         timeSinceOrigin.append((item['dt'] - originTime)/3600)
      windSpeed.append(item['wind_speed'])
      humidity.append(item['humidity'])
      temp.append(item['temp'])
      feelsLike.append(item['feels_like'])
      weather.append(item['weather'][0]['id']) 
   for item in resultOneCall['daily']:
      if not originTime:
         originTime = item['dt']
         daysSinceOrigin.append(0)
      else:
         daysSinceOrigin.append((item['dt'] - originTime)/(3600*24))
      rain.append(item.get('rain', 0))
      uvi.append(item.get('uvi', 0))
      snow.append(item.get('snow', 0))
      clouds.append(item.get('clouds', 0))
   summary.append("The wind speed will typically be between"
                  " %d to %d miles per hour" % (getLongestBreak(windSpeed)))
   summary.append("Humidity will typically vary between"
                  " %d to %d percent" % (getLongestBreak(humidity)))
   summary.append("Max temperature will be %d Fahrenheit" %(max(temp)))
   summary.append("Will feel like %d" %(max(feelsLike)))
   summary.append("Min temperature will be %d Fahrenheit" %(min(temp)))
   summary.append("Will feel like %d" %(min(feelsLike)))
   (rainIndex, value) = firstNonZeroIndexAndValue(rain) 
   if rainIndex != -1:
      summary.append("%d millimeter rain expected %s" %(value, turnIndexToDay(rainIndex)))
   (snowIndex, value) = firstNonZeroIndexAndValue(snow) 
   if snowIndex != -1:
      summary.append("%d millimeter snow expected %s" %(value, turnIndexToDay(snowIndex)))
   if rainIndex == -1 and snowIndex == -1:
      summary.append("No rain or snow expected in next 7 days")
   weatherType = [9 if i == 800 else i // 100 for i in weather]
   mostCommon = max(set(weatherType), key = weatherType.count)
   return (summary, translateToAnimation(mostCommon))

def on_user_intent(robot, event_type, event, done):
    user_intent = UserIntent(event)
    if user_intent.intent_event is UserIntentEvent.weather_response:
        data = json.loads(user_intent.intent_data)
        print (data)
        print(f"Weather report for {data['speakableLocationString']}: "
              f"{data['condition']}, temperature {data['temperature']} degrees")
        (summary, animation) = processWeather(data['speakableLocationString'])
        for item in summary:
           robot.behavior.say_text(item)
        robot.anim.play_animation(animation)
        done.set()


if __name__ == '__main__':
   with anki_vector.Robot() as robot:
      done = threading.Event()
      robot.events.subscribe(on_user_intent, Events.user_intent, done)
      print('------ Vector is waiting to be asked "Hey Vector!  What is the weather report?" Press ctrl+c to exit early ------')
      try:
         if not done.wait(timeout=60):
            print('------ Vector never heard a request for the weather report ------')
      except KeyboardInterrupt:
         pass

