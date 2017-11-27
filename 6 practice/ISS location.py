import urllib.request, json

url = "http://api.open-notify.org/iss-now.json"
try:
    response = json.load(urllib.request.urlopen(url))
except urllib.error.URLError:
    print('Ошибка: Соединение не установлено, проверьте подключение к Интернет')
    quit()
if response['message'] == "success":
    print("Соединение установлено")
    print("Координаты МКС:")
    print("Долгота: "+response['iss_position']['latitude'])
    print("Широта: "+response['iss_position']['longitude'])
else:
    print("Ошибка: Сервер не отвечает")






