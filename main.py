from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()

#start_date = os.environ['START_DATE']
#city = os.environ['CITY']
#birthday = os.environ['BIRTHDAY']

#app_id = os.environ["APP_ID"]
#app_secret = os.environ["APP_SECRET"]

#user_id = os.environ["USER_ID"]
#template_id = os.environ["TEMPLATE_ID"]

start_date = '2023-06-26'
city = '杭州'
birthday = '01-02'

app_id = 'wxb8d65642414c1c51'
app_secret = 'e0b897fa8edcaf4c8348bfcc4872a88d'

user_id = 'o6cMr6_Xkr6acU5b3w6-32pqirxU'
template_id = 'jwdy3rSTGzqUvQ1dvthNd5bM2v22mwd5VSszdLAgHbg'

def get_today():
  week_list = [ "星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
  today = datetime.now()
  return today.strftime("%Y-%m-%d") + '  ' + week_list[today.weekday()]

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_weather_new():
  url = "https://api.seniverse.com/v3/weather/daily.json?key=S3TT6fPbQKmCLF1VR&location=changsha&language=zh-Hans&unit=c&start=0&days=5"
  res = requests.get(url).json()
  weather = res['results'][0]['daily'][0]
  return weather['text_day'],int(weather['high']),int(weather['low'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  print (words.json()['data']['text'])
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature_h,temperature_l = get_weather_new()
#data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
data = {"td":{"value":get_today()},"weather":{"value":wea},"temperature_h":{"value":temperature_h},"temperature_l":{"value":temperature_l},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words()}}

res = wm.send_template(user_id, template_id, data)
print(res)
