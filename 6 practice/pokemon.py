import urllib.request, json

pokemon = input("Введите имя покемона на английском: ").lower()
url = "http://pokeapi.co/api/v2/pokemon/"
url = url+pokemon+'/'
request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.001'})
try:
    response = json.load(urllib.request.urlopen(request))
except urllib.error.HTTPError:
    print('Ошибка: Такого покемона нет')
    quit()
except urllib.error.URLError:
    print('Ошибка: Соединение не установлено, проверьте подключение к Интернет')
    quit()
print('Номер в покедексе: ' + str(response['id']))
print('Вес: '+str(response['weight']))
print('Рост: '+str(response['height']))
print('Тип:')
types = response['types']
for poke_type in types:
    print(poke_type['type']['name'])
print('Показатели:')
stats = response['stats']
for stat in stats:
    print(stat['stat']['name']+': '+str(stat['base_stat']))
print()
print('Способности: ')
abilities = response['abilities']
for ability in abilities:
    print(ability['ability']['name'])
print()
print('Приёмы: ')
moves = response['moves']
for move in moves:
    print(move['move']['name'])




