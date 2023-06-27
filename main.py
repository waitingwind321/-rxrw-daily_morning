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

app_id = 'wxc9a4535c3e6e81b8'
app_secret = 'adf67e020b54b7c4520a02ac23ecb6de'

user_id = 'ouqTY6KLFI_bSz1WPUfm4CqkCnOg'
template_id = 'ERxQV1zscSRsiTG_1Z5I_6mhLgwplvWHDC2QWpXGVbs'

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_weather_new():
  url = "https://api.seniverse.com/v3/weather/now.json?key=S3TT6fPbQKmCLF1VR&location=changsha&language=zh-Hans&unit=c"
  res = requests.get(url).json()
  weather = res['results'][0]['now']
  return weather['text'],math.floor(weather['temperature'])

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
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather_new()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
