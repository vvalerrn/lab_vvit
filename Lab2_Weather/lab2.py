import requests

city = "Moscow,RU"
appid = "d61c6794083aeee24001f5d5a109a574"
res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                   params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()

res_week = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                        params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data2 = res_week.json()

print('Город:', city)
print('Скорость ветра сегодня:', data['wind']['speed'])
print('Видимость сегодня:', data['visibility'])
for i in data2['list']:
    print('Дата:', i['dt_txt'], '\nСкорость ветра:', i['wind']['speed'], '\nВидимость:', i['visibility'])
    print('_________________________')